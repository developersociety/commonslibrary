from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.db.models import F
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.decorators.http import require_POST
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView

from comments.forms import CommentForm

from .choices import RESOURCE_WAITING_FOR_APPROVAL
from .forms import ResourceForm
from .models import Resource, ResourceCategory


class ResourceCreateView(LoginRequiredMixin, CreateView):
    form_class = ResourceForm
    template_name = 'resources/resource_form.html'
    success_url = reverse_lazy('resources:resource-thank-you')

    def form_valid(self, form):
        messages.success(
            self.request,
            'The {object} was added successfully. You may edit it again below.'.format(
                object=form.instance
            )
        )
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs


class ResourceDetailView(DetailView, CreateView):
    model = Resource
    form_class = CommentForm
    template_name = 'resources/resource_detail.html'

    def get_queryset(self):
        """
        Return approved resources unless requested user is approved and resource is waiting
        for approval.
        """
        qs = Resource.objects.approved(user=self.request.user).distinct()

        if self.request.user.is_authenticated:
            waiting_for_approval = Resource.objects.filter(
                created_by=self.request.user, status=RESOURCE_WAITING_FOR_APPROVAL
            ).distinct()
            qs = qs | waiting_for_approval

        return qs

    def dispatch(self, request, *args, **kwargs):
        slug = self.kwargs.get(self.slug_url_kwarg)
        if not Resource.objects.filter(slug=slug).exists():
            messages.error(
                request,
                "Whoops! This resource doesn't exist. Please try another search",
            )
            return HttpResponseRedirect(reverse('home'))
        elif not Resource.objects.approved(user=self.request.user).filter(slug=slug).exists():
            messages.error(
                request,
                (
                    "Whoops! This a private resource. If you're a member of the group this "
                    "resource belongs to, log in here "
                ),
            )
            return HttpResponseRedirect(
                '{url}?next={next}'.format(url=reverse('accounts:login'), next=request.path)
            )
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return self.get_object().get_absolute_url()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['related_resources'] = self.object.get_related(user=self.request.user)
        context['editable'] = self.request.user == self.object.created_by
        context['people_commented'] = self.object.comment_set.order_by().values_list(
            'created_by', flat=True
        ).distinct().count()

        if self.object.status == RESOURCE_WAITING_FOR_APPROVAL:
            context['waiting_for_approval'] = True

        self.object.hits = F('hits') + 1
        self.object.save(update_fields=['hits'])
        return context

    def form_invalid(self, form):
        # To prevent from crashing form_invalid should pass resource object instead of comment
        # empty one.
        self.object = self.get_object()
        return super().form_invalid(form)

    def get_initial(self):
        kwargs = super().get_initial()
        kwargs.update({'created_by': self.request.user})
        kwargs.update({'resource': self.object})
        return kwargs

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        # We want to set as None as self.object is not the instance in this case.
        kwargs['instance'] = None
        return kwargs

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Thank you for your comment')
        return response


class ResourceUpdateView(LoginRequiredMixin, UpdateView):
    model = Resource
    form_class = ResourceForm
    template_name = 'resources/resource_update.html'

    def get_success_url(self):
        return self.object.get_absolute_url()

    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)
        if obj.created_by != self.request.user:
            raise PermissionDenied(
                'No {verbose_name}s found matching the query'.format(
                    verbose_name=self.model._meta.verbose_name,
                )
            )
        return obj

    def form_valid(self, form):
        messages.success(self.request, 'Your resource has been updated')
        return super().form_valid(form=form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs


class ResourceCategoryListView(ListView):
    model = ResourceCategory

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        # monkey-patching, as calling the method from the template cannot send the request.user
        for category in context['resourcecategory_list']:
            category.get_approved_featured_resources = \
                category.get_approved_featured_resources(self.request.user)
        return context


class ResourceCategoryDetailView(DetailView):
    model = ResourceCategory

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        resource_category = context['resourcecategory']
        context['featured_resources'] = \
            resource_category.get_approved_featured_resources(self.request.user)
        return context


@require_POST
@staff_member_required
@permission_required('resources.change_resource')
def admin_categorise_resources_view(request):
    """
    Admin Action for assigning categories to resources.
    """
    m2m_relationship = Resource.categories.through
    resources = Resource.objects.filter(id__in=request.POST.get('resource_ids', '').split(','))
    categories = ResourceCategory.objects.filter(id__in=request.POST.getlist('category_ids', []))
    remove_categories = request.POST.get('remove') == '1'

    # Ensure permissions - this shouldn't be needed unless someone is being malicious:
    if not request.user.is_superuser and request.user.approved_organisations.exists():
        resources = resources.filter(organisation__in=request.user.approved_organisations.all()
                                     ).distinct()

    resource_ids = resources.values_list('id', flat=True)
    category_ids = categories.values_list('id', flat=True)

    if categories:
        with transaction.atomic():
            # As django 1.11 bulk_create doesn't have ignore_conflicts, the easiest way
            # is to delete any existing through_model, and then recreate them as needed.
            m2m_relationship.objects.filter(
                resource_id__in=resource_ids, resourcecategory_id__in=category_ids
            ).delete()

            if not remove_categories:
                m2m_relationship.objects.bulk_create((
                    m2m_relationship(resource_id=resource_id, resourcecategory_id=category_id)
                    for resource_id in resource_ids for category_id in category_ids
                ))

        messages.success(request, "{} resources updated".format(resources.count()))
    else:
        messages.info(request, "No Categories Selected")

    return HttpResponseRedirect(reverse('admin:resources_resource_changelist'))

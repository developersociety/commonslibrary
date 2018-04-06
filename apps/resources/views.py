from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import F
from django.urls import reverse_lazy
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView

from comments.forms import CommentForm

from .forms import ResourceForm
from .models import Resource


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
        return Resource.objects.approved(user=self.request.user)

    def get_success_url(self):
        return self.get_object().get_absolute_url()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['related_resources'] = self.object.get_related(user=self.request.user)
        context['people_commented'] = self.object.comment_set.order_by().values_list(
            'created_by', flat=True
        ).distinct().count()
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
        messages.success(self.request, 'Thank you for your comment.')
        return response

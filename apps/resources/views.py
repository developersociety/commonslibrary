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

    def get_success_url(self):
        return self.get_object().get_absolute_url()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.object.hits = F('hits') + 1
        self.object.save()
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['initial'].update({'created_by': self.request.user})
        kwargs['initial'].update({'resource': self.object})
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
        messages.success(self.request, 'Thank you for you comment.')
        return response

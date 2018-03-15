from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView

from .forms import UserRegistrationForm, UserUpdateForm
from .models import User


class UserCreateView(CreateView):
    form_class = UserRegistrationForm
    template_name = 'accounts/registration.html'
    # TODO: Temporary URL.
    success_url = '/'


class UserDetailView(LoginRequiredMixin, DetailView):
    model = User

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.object
        context['resources_created'] = user.resources_created.approved().count()
        context['resources_liked'] = user.resources_likes.approved().count()
        context['resources_tried'] = user.resources_tried.approved().count()
        return context

    def get_object(self, queryset=None):
        if self.request.user.is_authenticated:
            return self.request.user


class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserUpdateForm
    success_url = reverse_lazy('accounts:user-update')

    def get_object(self, queryset=None):
        if self.request.user.is_authenticated():
            return self.request.user

    def form_valid(self, form):
        messages.success(
            self.request,
            'The user profile was successfully. You may edit it again below.',
        )
        return super().form_valid(form)

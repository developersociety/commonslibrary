from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView

from .forms import UserRegistrationForm
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

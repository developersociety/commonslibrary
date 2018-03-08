from django.views.generic.edit import CreateView

from .forms import UserRegistrationForm


class UserCreateView(CreateView):
    form_class = UserRegistrationForm
    template_name = 'accounts/registration.html'
    # TODO: Temporary URL.
    success_url = '/'

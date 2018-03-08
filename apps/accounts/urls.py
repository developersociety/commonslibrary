from django.conf.urls import url
from django.contrib.auth.views import LoginView

from .forms import LoginForm
from .views import UserCreateView

app_name = 'accounts'
urlpatterns = [
    url(r'^registration/$', UserCreateView.as_view(), name='registration'),
    url(
        r'^login/$',
        LoginView.as_view(
            template_name='accounts/login.html',
            form_class=LoginForm,
        ),
        name='login'
    ),
]

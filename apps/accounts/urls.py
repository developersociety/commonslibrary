from django.urls import url
from django.contrib.auth import views
from django.core.urlresolvers import reverse_lazy

from .forms import LoginForm
from .views import UserCreateView

app_name = 'accounts'
urlpatterns = [
    url(r'^registration/$', UserCreateView.as_view(), name='registration'),
    url(
        r'^login/$',
        views.LoginView.as_view(
            template_name='accounts/login.html',
            form_class=LoginForm,
        ),
        name='login'
    ),
    url(r'^logout/$', views.LogoutView.as_view(), name='logout'),
    url(
        r'^password-reset/$',
        views.PasswordResetView.as_view(
            template_name='accounts/password_reset_form.html',
            email_template_name='accounts/emails/password_reset_email.html',
            success_url=reverse_lazy('accounts:password-reset-done'),
        ),
        name='password-reset',
    ),
    url(
        r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.PasswordResetConfirmView.as_view(
            template_name='accounts/password_reset_confirm.html',
            success_url=reverse_lazy('accounts:password-reset-complete'),
        ),
        name='password-reset-confirm'
    ),
    url(
        r'^password-reset/done/$',
        views.PasswordResetDoneView.as_view(template_name='accounts/password_reset_done.html'),
        name='password-reset-done'
    ),
    url(
        r'^reset/done/$',
        views.PasswordResetCompleteView.as_view(
            template_name='accounts/password_reset_complete.html'
        ),
        name='password-reset-complete',
    ),
]

from django.conf.urls import url
from django.contrib.auth import views
from django.urls import reverse_lazy

from pages.views import PageDetailView

from .forms import LoginForm, PasswordResetForm, SetPasswordForm, PasswordChangeForm
from .views import UserCreateView, UserDetailView, UserUpdateView

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
    url(
        r'^logout/$',
        views.LogoutView.as_view(
            template_name='accounts/logout.html',
        ),
        name='logout'
    ),
    url(
        r'^password-reset/$',
        views.PasswordResetView.as_view(
            email_template_name='accounts/emails/password_reset_email.html',
            form_class=PasswordResetForm,
            success_url=reverse_lazy('accounts:password-reset-done'),
            template_name='accounts/password_reset_form.html',
        ),
        name='password-reset',
    ),
    url(
        r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.PasswordResetConfirmView.as_view(
            form_class=SetPasswordForm,
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
    url(r'^profile/$', UserDetailView.as_view(), name='user-detail'),
    url(r'^update/$', UserUpdateView.as_view(), name='user-update'),
    url(
        r'^password-change/$',
        views.PasswordChangeView.as_view(
            template_name='accounts/password_change.html',
            form_class=PasswordChangeForm,
            success_url=reverse_lazy('accounts:user-detail')
        ),
        name='password-change',
    ),
    url(r'^thank-you/$', PageDetailView.as_view(), name='registration-thank-you'),
]

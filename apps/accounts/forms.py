from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.forms import (  # yapf: disable
    AuthenticationForm as BaseAuthenticatonForm, PasswordChangeForm as BasePasswordChangeForm,
    PasswordResetForm as BasePasswordResetForm, SetPasswordForm as BaseSetPasswordForm,
    UserChangeForm as BaseUserChangeForm, UserCreationForm as BaseUserCreationForm
)
from django.utils.safestring import mark_safe

from crispy_forms.helper import FormHelper
from crispy_forms.layout import HTML, ButtonHolder, Div, Field, Layout, Submit

from directory.models import Organisation

from .models import User


class AdminUserCreationForm(BaseUserCreationForm):

    class Meta:
        model = User
        fields = ('email',)


class AdminUserChangeForm(BaseUserChangeForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        user = self.request.user
        if user.is_staff and not user.is_superuser:
            # Sometimes is not there if it's set to readonly field in admin.py
            if 'approved_organisations' in self.fields:
                self.fields['approved_organisations'].queryset = user.approved_organisations.all()


class UserRegistrationForm(forms.ModelForm):

    error_messages = {
        'password_mismatch': "The two password fields didn't match.",
    }
    password = forms.CharField(
        widget=forms.PasswordInput,
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    confirm_password = forms.CharField(
        strip=False,
        widget=forms.PasswordInput,
    )
    privacy_agreement = forms.BooleanField(
        required=True,
        label='I agree to The Campaigns Library contacting me about my membership.',
        help_text=mark_safe(
            '''
            Your personal information will be held securely. By submitting information you are
            agreeing to the use of data and cookies in accordance with our
            <a href="/privacy/" target="_blank">privacy policy</a>.
            '''
        )
    )

    class Meta:
        model = User
        fields = (
            'email', 'password', 'confirm_password', 'first_name', 'last_name',
            'chosen_organisations', 'photo', 'phone', 'address'
        )
        labels = {
            'chosen_organisations': 'Groups',
        }
        help_texts = {
            'chosen_organisations':
                """
                Check all of the options that apply to you. If you don't belong to an existing
                group, please select 'Individual Changemaker'.
                """,
        }
        widgets = {
            'address': forms.TextInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['chosen_organisations'].widget = forms.CheckboxSelectMultiple()
        self.fields['chosen_organisations'].required = True

        self.helper = FormHelper()
        self.helper.layout = Layout(
            'email',
            'password',
            'confirm_password',
            'first_name',
            'last_name',
            'chosen_organisations',
            Div(
                Field('photo', css_class="sr__input"),
                Div(css_class='file-mount'),
                css_class='file-group'
            ),
            'phone',
            'address',
            'privacy_agreement',
            ButtonHolder(
                Submit('submit', 'Apply for access', css_class='submit'), css_class='form-actions'
            ),
        )

    def save(self, commit=True):
        password = self.cleaned_data['confirm_password']
        user = super().save(commit=False)
        user.set_password(password)
        if commit:
            user.save()
            self.grant_organisation(user)
            self.save_m2m()
        return user

    def grant_organisation(self, user):

        email_domain = user.get_email_domain()

        if Organisation.objects.filter(email__icontains=email_domain).exists():

            # more than one org can share the same email domain
            # find all organisations that have been selected in the form that also contain the
            # same email domain as the user
            organisations = Organisation.objects.filter(
                email__icontains=email_domain,
                pk__in=self.cleaned_data['chosen_organisations'].values_list("pk", flat=True)
            )

            # if orgs match the query, add the orgs who's email domain matches that of the user
            if organisations.exists():
                org_domain_matches = [
                    org for org in organisations if org.get_email_domain() == email_domain
                ]
                user.approved_organisations.add(*org_domain_matches)
        return user

    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password and confirm_password:
            if password != confirm_password:
                raise forms.ValidationError(
                    self.error_messages['password_mismatch'],
                    code='password_mismatch',
                )
        password_validation.validate_password(confirm_password)
        return confirm_password


class LoginForm(BaseAuthenticatonForm):

    def __init__(self, request=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'username', 'password',
            ButtonHolder(
                HTML(
                    """
                    <a href="{% url 'accounts:password-reset' %}">Forgot your password?</a>
                    """
                ),
                Submit('submit', 'Login', css_class='submit'),
                css_class='form-actions'
            ),
            HTML(
                """
                {% if next %}<input type="hidden" name="next" value="{{ next }}">{% endif %}
                """
            )
        )


class PasswordResetForm(BasePasswordResetForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False


class SetPasswordForm(BaseSetPasswordForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False


class UserUpdateForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'photo', 'phone', 'address')

    def __init__(self, request=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'first_name',
            'last_name',
            'email',
            Div(
                Field('photo', css_class="sr__input"),
                Div(css_class='file-mount'),
                css_class='file-group'
            ),
            'phone',
            'address',
            ButtonHolder(Submit('submit', 'Update', css_class='submit'), css_class='form-actions'),
        )


class PasswordChangeForm(BasePasswordChangeForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', 'Change'))

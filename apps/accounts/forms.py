from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.forms import (
    UserChangeForm as BaseUserChangeForm, UserCreationForm as BaseUserCreationForm
)

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from .models import User


class UserCreationForm(BaseUserCreationForm):

    class Meta:
        model = User
        fields = ('email',)


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

    class Meta:
        model = User
        fields = (
            'email', 'password', 'confirm_password', 'first_name', 'last_name', 'organisations',
            'photo', 'phone', 'address'
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['address'].widget = forms.TextInput()
        self.fields['organisations'].widget = forms.CheckboxSelectMultiple()
        self.fields['organisations'].required = True

        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', 'Submit'))

    def save(self, commit=True):
        password = self.cleaned_data['confirm_password']
        user = super().save(commit=False)
        user.set_password(password)
        if commit:
            user.save()
            self.save_m2m()
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


class UserChangeForm(BaseUserChangeForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        user = self.request.user
        if user.is_staff and not user.is_superuser:
            # Sometimes is not there if it's set to readonly field in admin.py
            if 'approved_organisations' in self.fields:
                self.fields['approved_organisations'].queryset = user.approved_organisations.all()

from django.contrib.auth.forms import (
    UserChangeForm as BaseUserChangeForm, UserCreationForm as BaseUserCreationForm
)

from .models import User


class UserCreationForm(BaseUserCreationForm):

    class Meta:
        model = User
        fields = ('email',)


class UserChangeForm(BaseUserChangeForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        user = self.request.user
        if user.is_staff and not user.is_superuser:
            # Sometimes is not there if it's set to readonly field in admin.py
            if 'approved_organisations' in self.fields:
                self.fields['approved_organisations'].queryset = user.approved_organisations.all()

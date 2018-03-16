from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from .models import Resource


class ResourceForm(forms.ModelForm):

    class Meta:
        model = Resource
        fields = ('title', 'abstract', 'content', 'tags', 'image', 'organisation', 'privacy')

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        self.fields['organisation'].queryset = user.approved_organisations.all()
        self.fields['privacy'].queryset = user.approved_organisations.all()
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', 'Submit'))

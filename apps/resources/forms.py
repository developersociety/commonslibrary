from django import forms
from django.utils.text import slugify

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from .models import Resource


class ResourceForm(forms.ModelForm):

    class Meta:
        model = Resource
        fields = ('title', 'abstract', 'content', 'tags', 'image', 'organisation', 'privacy')

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        self.fields['organisation'].queryset = self.user.approved_organisations.all()
        self.fields['privacy'].queryset = self.user.approved_organisations.all()
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', 'Submit'))

    def save(self, commit=True):
        self.instance.created_by = self.user
        self.instance.updated_by = self.user
        self.instance.slug = slugify(self.title)
        return super().save(commit=commit)

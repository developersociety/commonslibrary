from django import forms
from django.utils.text import slugify

from crispy_forms.helper import FormHelper
from crispy_forms.layout import ButtonHolder, Div, Field, Layout, Submit

from .models import Resource


class ResourceForm(forms.ModelForm):

    class Meta:
        model = Resource
        fields = ('title', 'abstract', 'content', 'tags', 'image', 'organisation', 'privacy')
        labels = {'organisation': 'Group'}

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        self.fields['abstract'].widget.attrs['rows'] = 3
        self.fields['organisation'].queryset = self.user.approved_organisations.all()
        self.fields['privacy'].queryset = self.user.approved_organisations.all()
        self.fields['privacy'].widget = forms.CheckboxSelectMultiple()
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'title',
            'abstract',
            'content',
            Div(
                Field('tags', css_class="sr__input"),
                Div(css_class='tag-select'),
                css_class='tag-group'
            ),
            Div(
                Field('image', css_class="sr__input"),
                Div(css_class='file-mount'),
                css_class='file-group'
            ),
            'organisation',
            'privacy',
            ButtonHolder(
                Submit('submit', 'Submit your resource', css_class='submit'),
                css_class='form-actions'
            ),
        )

    def save(self, commit=True):
        self.instance.created_by = self.user
        self.instance.updated_by = self.user
        self.instance.slug = slugify(self.instance.title)
        return super().save(commit=commit)

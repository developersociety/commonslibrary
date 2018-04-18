from django import forms
from django.utils.text import slugify

from crispy_forms.helper import FormHelper
from crispy_forms.layout import ButtonHolder, Div, Field, Layout, Submit

from .models import Resource


class ResourceForm(forms.ModelForm):
    is_public = forms.BooleanField(label='Make this resource public', initial=True)

    class Meta:
        model = Resource
        fields = ('title', 'abstract', 'content', 'tags', 'image', 'organisation', 'privacy')
        labels = {'organisation': 'Group'}

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        self.fields['abstract'].widget.attrs['rows'] = 3
        self.fields['organisation'].queryset = self.user.approved_organisations.all()
        self.fields['organisation'].empty_label = 'Select'
        self.fields['privacy'].queryset = self.user.approved_organisations.all()
        self.fields['privacy'].widget = forms.CheckboxSelectMultiple()
        self.fields['privacy'].initial = [privacy[0] for privacy in self.fields['privacy'].choices]

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
            'is_public',
            'privacy',
            ButtonHolder(
                Submit('submit', 'Submit your resource', css_class='submit'),
                css_class='form-actions resource-form-actions'
            ),
        )

    def save(self, commit=True):
        self.instance.created_by = self.user
        self.instance.updated_by = self.user
        self.instance.slug = slugify(self.instance.title)

        # If user selected make resource public make sure we emptying the privacy choices.
        if self.cleaned_data['is_public']:
            self.cleaned_data['privacy'] = ''
        return super().save(commit=commit)

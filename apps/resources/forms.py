from django import forms
from django.utils.text import slugify

from crispy_forms.helper import FormHelper
from crispy_forms.layout import ButtonHolder, Div, Field, Layout, Submit

from .models import Resource


class ResourceForm(forms.ModelForm):
    is_public = forms.BooleanField(label='Make this resource public', initial=True, required=False)

    class Meta:
        model = Resource
        fields = ('title', 'abstract', 'content', 'tags', 'image', 'organisation', 'privacy')
        labels = {
            'organisation': 'Group',
            'privacy': 'Of your groups, who can view it?',
        }
        help_texts = {
            'content': (
                """
                Use this for the main body of your resource – you can embed online documents
                using HTML in "Source" and add drop down accordions using "MJ Accordions
                """
            ),
            'privacy':
                'The group you belong to is selected by default',
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')

        super().__init__(*args, **kwargs)

        if self.instance.id:
            button_title = 'Update your resource'
        else:
            button_title = 'Submit your resource'

        self.fields['abstract'].widget.attrs['rows'] = 3
        self.fields['organisation'].queryset = self.user.approved_organisations.all()
        self.fields['organisation'].empty_label = 'Select'
        self.fields['privacy'].queryset = self.user.approved_organisations.all()
        self.fields['privacy'].widget = forms.CheckboxSelectMultiple()
        self.fields['privacy'].initial = [id for id, option in self.fields['privacy'].choices]

        self.helper = FormHelper()
        self.helper.layout = Layout(
            'title',
            'abstract',
            'content',
            Field('category'),
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
            Field('privacy', wrapper_class="sr__input"),
            ButtonHolder(
                Submit('submit', button_title, css_class='submit'),
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

    def clean_title(self):
        title = self.cleaned_data['title']
        if self.instance.id:
            if Resource.objects.filter(slug=slugify(title)).exclude(id=self.instance.id).exists():
                raise forms.ValidationError('Resource with this title already exists')
        else:
            if Resource.objects.filter(slug=slugify(title)).exists():
                raise forms.ValidationError('Resource with this title already exists')
        return title

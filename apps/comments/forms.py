from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import ButtonHolder, Layout, Submit

from .models import Comment, Report


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('body', 'created_by', 'resource',)
        widgets = {
            'created_by': forms.HiddenInput,
            'resource': forms.HiddenInput,
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'body',
            'created_by',
            'resource',
            ButtonHolder(Submit('submit', 'Submit', css_class='submit'), css_class='form-actions'),
        )


class ReportForm(forms.ModelForm):

    class Meta:
        model = Report
        fields = ('body', 'created_by', 'comment',)
        widgets = {
            'created_by': forms.HiddenInput,
            'comment': forms.HiddenInput,
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'body',
            'created_by',
            'comment',
            ButtonHolder(Submit('submit', 'Submit', css_class='submit'), css_class='form-actions'),
        )

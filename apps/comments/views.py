from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView

from .forms import CommentForm, ReportForm
from .models import Comment


class ReportCommentView(LoginRequiredMixin, DetailView, CreateView):
    model = Comment
    form_class = ReportForm
    slug_url_kwarg = 'id'
    slug_field = 'id'
    template_name = 'comments/report_form.html'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)
        if obj.created_by == self.request.user:
            raise PermissionDenied(
                'No {verbose_name}s found matching the query'.format(
                    verbose_name=self.model._meta.verbose_name,
                )
            )
        return obj

    def get_success_url(self):
        return self.object.comment.resource.get_absolute_url()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_initial(self):
        kwargs = super().get_initial()
        kwargs.update({'comment': self.object})
        kwargs.update({'created_by': self.request.user})
        return kwargs

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['instance'] = None
        return kwargs

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Thank you the comment was reported.')
        return response


class CommentUpdateView(LoginRequiredMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    slug_url_kwarg = 'id'
    slug_field = 'id'
    template_name = 'comments/comment_update.html'

    def get_success_url(self):
        return self.object.resource.get_absolute_url()

    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)
        if obj.created_by != self.request.user:
            raise PermissionDenied(
                'No {verbose_name}s found matching the query'.format(
                    verbose_name=self.model._meta.verbose_name,
                )
            )
        return obj

    def form_valid(self, form):
        messages.success(self.request, 'Your comment has been updated.')
        return super().form_valid(form=form)

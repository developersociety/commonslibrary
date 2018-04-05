from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView

from .forms import ReportForm
from .models import Comment


class ReportCommentView(LoginRequiredMixin, DetailView, CreateView):
    model = Comment
    form_class = ReportForm
    slug_url_kwarg = 'id'
    slug_field = 'id'
    template_name = 'comments/report_form.html'

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
from django.conf import settings
from django.http import Http404, HttpResponsePermanentRedirect
from django.shortcuts import get_object_or_404
from django.views.generic.detail import DetailView

from .models import Page


class PageDetailView(DetailView):
    model = Page
    template_name = 'pages/detail.html'
    slug_url_kwarg = 'url'
    slug_field = 'url'

    def get_object(self, queryset=None):
        url = self.kwargs.get(self.slug_url_kwarg) or self.request.path
        if not url.startswith('/'):
            url = '/' + url

        try:
            obj = get_object_or_404(self.model, url=url, is_active=True)
        except Http404:
            if not url.endswith('/') and settings.APPEND_SLASH:
                url += '/'
                obj = get_object_or_404(self.model, url=url, is_active=True)
                return HttpResponsePermanentRedirect('{slug}/'.format(slug=self.request.path))
            else:
                raise
        return obj

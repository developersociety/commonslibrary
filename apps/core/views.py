from django.views.generic import TemplateView

from resources.models import Resource

from .mixins import ArticlesViewMixin


class HomeView(TemplateView, ArticlesViewMixin):
    template_name = 'core/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['carousel_resources'] = Resource.get_carousel_resources(self.request.user)
        return context


class SearchView(TemplateView, ArticlesViewMixin):
    template_name = 'core/search.html'

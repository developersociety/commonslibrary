from django.views.generic import TemplateView

from accounts.models import User
from directory.models import Organisation
from pages.models import Page
from resources.models import Resource
from tags.models import Tag

from .mixins import ResourcesViewMixin


class HomeView(TemplateView, ResourcesViewMixin):
    template_name = 'core/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['carousel_resources'] = Resource.get_carousel_resources(self.request.user)
        return context


class SearchView(TemplateView, ResourcesViewMixin):
    template_name = 'core/search.html'


class ExploreView(TemplateView):
    template_name = 'explore/explore_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['people'] = User.objects.all().order_by('first_name')
        context['groups'] = Organisation.objects.all().order_by('title')
        context['tags'] = Tag.objects.all()
        context['pages'] = Page.objects.filter(is_active=True)
        return context

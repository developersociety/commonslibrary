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
        context['latest_resource'] = Resource.get_latest(self.request.user)
        most_tried_resource = Resource.get_most_tried(self.request.user).first()
        context['most_tried'] = most_tried_resource
        kwargs = {'user': self.request.user}
        if most_tried_resource:
            kwargs.update({'exclude': most_tried_resource.id})
        context['most_liked'] = Resource.get_most_liked(**kwargs).first()
        context['most_published'] = Organisation.get_most_published_this_week()
        return context


class SearchView(TemplateView, ResourcesViewMixin):
    template_name = 'core/search.html'


class ExploreView(TemplateView):
    template_name = 'explore/explore_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tags'] = Tag.objects.all()
        context['pages'] = Page.objects.filter(is_active=True)
        return context

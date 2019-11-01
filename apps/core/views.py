from django.views.generic import TemplateView

from directory.models import Organisation
from resources.models import Resource

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

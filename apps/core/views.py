from django.views.generic import TemplateView

from directory.models import Organisation
from resources.models import Resource


class HomeView(TemplateView):
    template_name = 'core/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['carousel_resources'] = Resource.get_carousel_resources(self.request.user)
        context['latest_resource'] = Resource.get_latest(self.request.user)
        context['most_liked_resource'] = Resource.get_most_liked(self.request.user)
        context['most_tried_resource'] = Resource.get_most_tried(self.request.user)
        context['most_published'] = Organisation.get_most_published_this_week()
        context['latest_resources'] = Resource.objects.approved(
            self.request.user,
        ).order_by(
            '-created_at',
        )[:12]
        return context

from directory.models import Organisation
from resources.models import Resource


class ResourcesViewMixin(object):

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
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

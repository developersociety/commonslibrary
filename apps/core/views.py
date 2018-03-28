from django.views.generic import TemplateView

from resources.models import Resource


class HomeView(TemplateView):
    template_name = 'core/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['carousel_resources'] = Resource.get_carousel_resources(self.request.user)
        return context

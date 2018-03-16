from django.views.generic.detail import DetailView

from .models import Organisation


class OrganisationDetailView(DetailView):
    model = Organisation

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

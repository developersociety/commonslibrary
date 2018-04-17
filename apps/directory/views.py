from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from accounts.models import User

from .models import Organisation


class OrganisationListView(ListView):
    model = Organisation
    ordering = ['title']


class OrganisationDetailView(DetailView):
    model = Organisation

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class OrganisationUserView(DetailView):
    model = User

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = context['user']
        context['resources_created'] = user.resources_created.approved().count()
        context['resources_liked'] = user.resources_likes.approved().count()
        context['resources_tried'] = user.resources_tried.approved().count()
        return context

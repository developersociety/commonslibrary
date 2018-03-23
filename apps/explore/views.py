from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from accounts.models import User
from directory.models import Organisation
from tags.models import Tag


class ExploreView(ListView):
    template_name = 'explore/explore_list.html'
    model = Tag

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['people'] = User.objects.all().order_by('first_name')
        context['groups'] = Organisation.objects.all().order_by('title')
        return context

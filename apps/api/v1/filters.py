import django_filters
from django_filters.rest_framework import FilterSet

from accounts.models import User
from directory.models import Organisation
from resources.models import Resource


class ResourceFilter(FilterSet):
    organisation = django_filters.filters.ModelMultipleChoiceFilter(
        queryset=Organisation.objects.all()
    )
    created_by = django_filters.filters.ModelMultipleChoiceFilter(queryset=User.objects.all())

    class Meta:
        model = Resource
        fields = ('tags', 'organisation', 'created_by',)

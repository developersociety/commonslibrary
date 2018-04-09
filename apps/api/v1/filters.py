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
    most_likes = django_filters.filters.OrderingFilter(
        # tuple-mapping retains order
        fields=(('most_likes', 'resource'),),

        # labels do not need to retain order
        field_labels={
            'most_likes': 'Most likes',
        }
    )

    class Meta:
        model = Resource
        fields = ('tags', 'organisation', 'created_by')

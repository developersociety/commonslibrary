import django_filters
from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector
from django_filters.rest_framework import FilterSet

from accounts.models import User
from directory.models import Organisation
from resources.models import Resource
from tags.models import Tag

RANK_CUTOFF = 0.000001

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
    most_tried = django_filters.filters.OrderingFilter(
        # tuple-mapping retains order
        fields=(('most_tried', 'resource'),),

        # labels do not need to retain order
        field_labels={
            'most_tried': 'Most tried',
        }
    )
    tags = django_filters.filters.ModelMultipleChoiceFilter(
        queryset=Tag.objects.all(),
        conjoined=True,
    )
    q = django_filters.CharFilter(label="Search", method="delay_search")

    class Meta:
        model = Resource
        fields = ('categories', 'organisation', 'created_by')

    def delay_search(self, queryset, name, value):
        self._search_query = value
        return queryset

    @property
    def qs(self):
        qs = super().qs
        search_query = getattr(self, "_search_query", None)
        if search_query:
            query = SearchQuery(search_query)
            vectors =  SearchVector("title", weight="A") + SearchVector("abstract", weight="B") + SearchVector("tags__title", weight="C")

            return  (
                qs.annotate(search_rank=SearchRank(vectors, query))
                .filter(search_rank__gt=RANK_CUTOFF)
                .order_by("-search_rank")
            )

        return qs

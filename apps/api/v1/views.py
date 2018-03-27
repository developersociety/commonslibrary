from django.db.models import Q

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets

from resources.models import Resource

from .serializers import ResourceSerializer


class ResourceViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ResourceSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    filter_fields = (
        'id', 'title', 'abstract', 'content', 'created_by', 'organisation', 'privacy',
    )
    search_fields = ('title', 'abstract',)

    def get_queryset(self):
        print(self.request.META.get('REMOTE_USER'))
        user = self.request.user
        if user.is_authenticated():
            if user.is_superuser:
                qs = Resource.objects.approved().select_related(
                    'organisation',
                    'created_by',
                ).prefetch_related(
                    'likes',
                    'tried',
                )
            elif user.approved_organisations.exists():
                qs = Resource.objects.select_related(
                    'organisation',
                    'created_by',
                ).prefetch_related(
                    'likes',
                    'tried',
                ).filter(
                    Q(is_approved=True) | Q(privacy__in=user.approved_organisations.all()),
                ).distinct()
        else:
            qs = Resource.objects.approved().select_related(
                'organisation',
                'created_by',
            ).prefetch_related(
                'likes',
                'tried',
            ).filter(
                privacy__isnull=True,
            )
        return qs

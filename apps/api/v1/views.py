from distutils.util import strtobool

from django.db.models import Q
from django.http.response import Http404

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, viewsets
from rest_framework.response import Response

from accounts.models import User
from directory.models import Organisation
from resources.models import Resource
from tags.models import Tag

from .permissions import ResourcePermission
from .serializers import OrganisationSerializer, ResourceSerializer, TagSerializer, UserSerializer


class ResourceViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ResourceSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    permission_classes = (ResourcePermission,)
    filter_fields = ('organisation', 'privacy',)
    search_fields = ('title', 'abstract',)

    def get_queryset(self):
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

    def update(self, request, pk=None):
        try:
            obj = self.get_object()
        except Http404:
            # Using 406 as the 404 causes middleware issues for the pages.
            response = Response(status=status.HTTP_406_NOT_ACCEPTABLE)
        else:
            if 'like' in request.data:
                like = strtobool(request.data.get('like'))
                if like:
                    obj.likes.add(request.user)
                else:
                    obj.likes.remove(request.user)
                response = Response(status=status.HTTP_202_ACCEPTED)
            elif 'tried' in request.data:
                tried = strtobool(request.data.get('tried'))
                if tried:
                    obj.tried.add(request.user)
                else:
                    obj.tried.remove(request.user)
                response = Response(status=status.HTTP_202_ACCEPTED)
            else:
                response = Response(status=status.HTTP_403_FORBIDDEN)
        return response


class OrganisationViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Organisation.objects.all()
    serializer_class = OrganisationSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('id', 'title',)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('id', 'title',)


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('id', 'first_name', 'last_name')

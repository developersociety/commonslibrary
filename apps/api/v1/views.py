from django.db import models

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, viewsets
from rest_framework.decorators import detail_route
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from accounts.models import User
from directory.models import Organisation
from resources.models import Resource
from tags.models import Tag

from .filters import ResourceFilter
from .serializers import OrganisationSerializer, ResourceSerializer, TagSerializer, UserSerializer


class ResourceViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ResourceSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filter_class = ResourceFilter
    search_fields = ('title', 'abstract',)
    permission_classes = (AllowAny,)

    def get_queryset(self):
        user = self.request.user
        qs = Resource.objects.approved(user).annotate(
            most_likes=models.Count('likes'),
            most_tried=models.Count('tried')
        ).select_related(
            'organisation',
            'created_by',
        ).prefetch_related(
            'likes',
            'tried',
        )
        return qs

    @detail_route(methods=['put'], permission_classes=[IsAuthenticated])
    def tried(self, request, pk=None):
        obj = self.get_object()
        if request.user in obj.tried.all():
            obj.tried.remove(request.user)
        else:
            obj.tried.add(request.user)
        return Response(status=status.HTTP_202_ACCEPTED)

    @detail_route(methods=['put'], permission_classes=[IsAuthenticated])
    def like(self, request, pk=None):
        obj = self.get_object()
        if request.user in obj.likes.all():
            obj.likes.remove(request.user)
        else:
            obj.likes.add(request.user)
        return Response(status=status.HTTP_202_ACCEPTED)


class OrganisationViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Organisation.objects.all()
    serializer_class = OrganisationSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('id', '^title',)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter,)
    filter_fields = ('id',)
    search_fields = ('id', '^title',)


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('id', '^first_name', '^last_name')

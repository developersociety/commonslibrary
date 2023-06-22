from django.db import models

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, viewsets
from rest_framework.decorators import detail_route, list_route
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from accounts.models import User
from directory.models import Organisation
from resources.models import Resource
from tags.models import Tag

from .filters import ResourceFilter
from .paginations import ResourcesPagination
from .serializers import (
    OrganisationSerializer, ResourceFavouriteSerializer, ResourceSerializer, TagSerializer,
    UserSerializer
)


class ResourceViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ResourceSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filter_class = ResourceFilter
    pagination_class = ResourcesPagination
    search_fields = (
        'title', 'abstract', 'created_by__first_name', 'created_by__last_name',
        'organisation__title', 'tags__title'
    )
    permission_classes = (AllowAny,)

    def get_queryset(self):
        user = self.request.user
        qs = Resource.objects.approved(user).annotate(
            most_likes=models.Count('likes'), most_tried=models.Count('tried')
        ).select_related(
            'organisation',
            'created_by',
        ).prefetch_related(
            'likes',
            'tried',
            'privacy',
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

    @list_route(methods=['get'])
    def favourites(self, request, pk=None):
        data = {}
        # Latest resource
        latest_resource = Resource.get_latest(self.request.user)
        latest_resource_ser = ResourceSerializer(
            instance=latest_resource, context={'request': request}
        )
        data['latest_resource'] = latest_resource_ser.data

        # Most tried
        most_tried = Resource.get_most_tried(self.request.user).first()
        most_tried_ser = ResourceSerializer(instance=most_tried, context={'request': request})
        data['most_tried'] = most_tried_ser.data

        # Most liked
        most_liked = Resource.get_most_liked().first()
        most_liked_ser = ResourceSerializer(instance=most_liked, context={'request': request})
        data['most_liked'] = most_liked_ser.data

        # Most published
        most_published = Organisation.get_most_published_this_week()
        most_published_ser = OrganisationSerializer(
            instance=most_published, context={'request': request}
        )
        data['most_published'] = most_published_ser.data



        return Response(data)


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

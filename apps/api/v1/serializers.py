from django.urls import reverse

from rest_framework import serializers
from sorl.thumbnail import get_thumbnail

from accounts.models import User
from directory.models import Organisation
from resources.models import Resource
from tags.models import Tag


class ResourceSerializer(serializers.ModelSerializer):
    organisation = serializers.CharField(source='organisation.title', read_only=True)
    image = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()
    tried_count = serializers.SerializerMethodField()
    url = serializers.SerializerMethodField()
    created_by = serializers.SerializerMethodField()
    created_by_link = serializers.SerializerMethodField()
    organisation_logo = serializers.SerializerMethodField()
    is_private = serializers.SerializerMethodField()

    class Meta:
        model = Resource
        fields = (
            'id', 'title', 'image', 'abstract', 'organisation', 'likes_count', 'tried_count',
            'hits', 'url', 'created_by', 'created_by_link', 'organisation_logo', 'is_private',
        )

    def get_likes_count(self, obj):
        return obj.likes.count()

    def get_tried_count(self, obj):
        return obj.tried.count()

    def get_url(self, obj):
        return obj.get_absolute_url()

    def get_created_by(self, obj):
        return obj.created_by.get_full_name()

    def get_created_by_link(self, obj):
        return reverse('directory:organisation-user', kwargs={'pk': obj.created_by.pk})

    def get_image(self, obj):
        thumb = get_thumbnail(obj.image, '800', quality=99)
        if thumb:
            return thumb.url

    def get_organisation_logo(self, obj):
        thumb = get_thumbnail(obj.organisation.logo, '150', quality=99)
        if thumb:
            return thumb.url

    def get_is_private(self, obj):
        return obj.privacy.exists()


class OrganisationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Organisation
        fields = ('id', 'title',)


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ('id', 'title',)


class UserSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'title',)

    def get_title(self, obj):
        return obj.get_full_name()

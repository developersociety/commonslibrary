from rest_framework import serializers
from sorl.thumbnail import get_thumbnail

from directory.models import Organisation
from resources.models import Resource


class ResourceSerializer(serializers.ModelSerializer):
    organisation = serializers.CharField(source='organisation.title', read_only=True)
    image = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()
    tried_count = serializers.SerializerMethodField()
    url = serializers.SerializerMethodField()
    created_by = serializers.SerializerMethodField()
    organisation_logo = serializers.SerializerMethodField()
    is_private = serializers.SerializerMethodField()

    class Meta:
        model = Resource
        fields = (
            'id', 'title', 'image', 'abstract', 'organisation', 'likes_count', 'tried_count',
            'hits', 'url', 'created_by', 'organisation_logo', 'is_private',
        )

    def get_likes_count(self, obj):
        return obj.likes.count()

    def get_tried_count(self, obj):
        return obj.tried.count()

    def get_url(self, obj):
        return obj.get_absolute_url()

    def get_created_by(self, obj):
        return obj.created_by.get_full_name()

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

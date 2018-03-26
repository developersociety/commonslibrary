from rest_framework import serializers

from resources.models import Resource


class ResourceSerializer(serializers.ModelSerializer):
    organisation = serializers.CharField(source='organisation.title', read_only=True)
    likes_count = serializers.SerializerMethodField()
    tried_count = serializers.SerializerMethodField()
    url = serializers.SerializerMethodField()

    class Meta:
        model = Resource
        fields = (
            'title', 'abstract', 'organisation', 'likes_count', 'tried_count', 'hits', 'url',
        )

    def get_likes_count(self, obj):
        return obj.likes.count()

    def get_tried_count(self, obj):
        return obj.tried.count()

    def get_url(self, obj):
        return obj.get_absolute_url()

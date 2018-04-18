from datetime import timedelta
from urllib.parse import urlparse

from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils import timezone

from ckeditor_uploader.fields import RichTextUploadingField
from colorfield.fields import ColorField
from sorl.thumbnail import ImageField

from resources.choices import RESOURCE_APPROVED
from resources.models import Resource


class Organisation(models.Model):
    title = models.CharField(max_length=256, unique=True)
    colour = ColorField(default='#50E3C2')
    url = models.URLField(blank=True)
    slug = models.SlugField(unique=True, null=True)
    telephone = models.CharField(max_length=16, blank=True)
    address = RichTextUploadingField(blank=True)
    description = RichTextUploadingField(blank=True)
    logo = ImageField(blank=True, upload_to='uploads/directory/organisation/%Y/%m/%d')
    email = models.EmailField(blank=True)
    founder = models.BooleanField(default=False)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='organisations_created'
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='organisations_updated'
    )
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('directory:organisation-detail', kwargs={'slug': self.slug})

    def get_short_url(self):
        return urlparse(self.url).netloc[4:]

    def get_total_private_resources_count(self):
        return self.resources_privacy.approved().count()

    def get_most_tried_resource(self):
        return self.resource_set.approved().annotate(
            most_tried=models.Count('tried'),
        ).order_by(
            '-most_tried',
        ).first()

    def get_most_liked_resource(self):
        return self.resource_set.approved().annotate(
            most_liked=models.Count('likes'),
        ).order_by(
            '-most_liked',
        ).first()

    def get_latest_resource(self):
        try:
            resource = self.resource_set.approved().earliest('created_at')
        except Resource.DoesNotExist:
            resource = None
        return resource

    @staticmethod
    def get_most_published_this_week():
        """ Returns the organisation which published most resources this week. """
        return Organisation.objects.filter(
            resource__created_at__gte=timezone.now() - timedelta(days=7),
            resource__status=RESOURCE_APPROVED,
        ).annotate(
            most_published=models.Count('resource'),
        ).order_by(
            '-most_published',
        ).first()

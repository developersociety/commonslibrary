from django.conf import settings
from django.db import models

from ckeditor.fields import RichTextField
from sorl.thumbnail import ImageField

from directory.models import Organisation
from tags.models import Tag


class Resource(models.Model):
    title = models.CharField(max_length=256, unique=True)
    abstract = models.TextField(
        max_length=140,
        help_text='This text will appear in search results',
    )
    content = RichTextField()
    tags = models.ManyToManyField(
        Tag,
        limit_choices_to=models.Q(level=1) | models.Q(level=2),
        blank=True,
    )
    image = ImageField(
        'Background Image',
        upload_to='uploads/resources/images/%Y/%m/%d',
        blank=True,
    )
    organisation = models.ForeignKey(
        Organisation,
        help_text='Of the groups you belong to, which one owns this resource?',
    )
    privacy = models.ManyToManyField(
        Organisation,
        help_text='Of the groups you belong to, which should this resource be visible to?',
        related_name='resources_privacy',
        blank=True,
    )
    is_approved = models.BooleanField(default=False)

    likes = models.ManyToManyField(
        settings.AUTH_USER_MODEL, blank=True, related_name='resources_likes'
    )
    tried = models.ManyToManyField(
        settings.AUTH_USER_MODEL, blank=True, related_name='resources_tried'
    )
    hits = models.PositiveIntegerField('How many times page been hit?', default=0)

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='resources_created'
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='resources_updated'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return self.title

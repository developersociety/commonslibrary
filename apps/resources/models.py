from django.conf import settings
from django.db import models
from django.urls import reverse

from ckeditor.fields import RichTextField
from sorl.thumbnail import ImageField

from tags.models import Tag

from .managers import ResourceManager


class Resource(models.Model):
    title = models.CharField(max_length=256, unique=True)
    slug = models.SlugField(unique=True, null=True)
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
        'directory.Organisation',
        help_text='Of the groups you belong to, which one owns this resource?',
        on_delete=models.SET_NULL,
        null=True,
    )
    privacy = models.ManyToManyField(
        'directory.Organisation',
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

    objects = ResourceManager()

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('resources:resource-detail', kwargs={'slug': self.slug})

    def private_for_organisation(self, organisation):
        return organisation in self.privacy.all()

    @staticmethod
    def get_carousel_resources(user):
        approved_resources = Resource.objects.approved(user)
        return approved_resources

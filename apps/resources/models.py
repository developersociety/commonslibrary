from datetime import timedelta

from django.conf import settings
from django.db import models
from django.db.models import Case, When
from django.db.models.functions import Cast
from django.urls import reverse
from django.utils import timezone

from adminsortable.models import SortableMixin
from ckeditor_uploader.fields import RichTextUploadingField
from sorl.thumbnail import ImageField

from tags.models import Tag

from . import choices
from .managers import ResourceManager


class Resource(models.Model):
    title = models.CharField(max_length=140, unique=True)
    slug = models.SlugField(unique=True, null=True, max_length=140)
    abstract = models.TextField(
        max_length=140,
        help_text='This text will appear in search results',
    )
    content = RichTextUploadingField()
    categories = models.ManyToManyField('resources.ResourceCategory')
    tags = models.ManyToManyField(Tag, blank=True)
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
    status = models.IntegerField(
        choices=choices.RESOURCES_STATUSES, default=choices.RESOURCE_WAITING_FOR_APPROVAL
    )
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
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    objects = ResourceManager()

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        url = ''
        if self.slug:
            url = reverse('resources:resource-detail', kwargs={'slug': self.slug})
        return url

    def private_for_organisation(self, organisation):
        return organisation in self.privacy.all()

    @staticmethod
    def get_carousel_resources(user=None, limit=5):
        """ Get most popular resources for the last 7 days. """
        resources = Resource.objects.approved(user=user).filter(
            created_at__gte=timezone.now() - timedelta(days=7)
        ).annotate(
            popular_count=(
                Cast(models.Count('tried'), models.PositiveIntegerField()) +
                Cast(models.Count('likes'), models.PositiveIntegerField()) + models.F('hits')
            )
        ).order_by('-popular_count')[:limit]
        return resources

    @staticmethod
    def get_latest(user=None):
        try:
            resource = Resource.objects.approved(user=user).earliest('created_at')
        except Resource.DoesNotExist:
            resource = None
        return resource

    @staticmethod
    def get_most_liked(user=None, exclude=None, limit=1):
        resources = Resource.objects.approved(user=user).exclude(id=exclude).annotate(
            most_liked=models.Count('likes')
        ).order_by(
            '-most_liked',
        )[:limit]
        return resources

    @staticmethod
    def get_most_tried(user=None, exclude=None, limit=1):
        resources = Resource.objects.approved(user=user).exclude(id=exclude).annotate(
            most_tried=models.Count('tried')
        ).order_by(
            '-most_tried',
        )[:limit]
        return resources

    def get_related(self, user=None, limit=3):
        data = {}
        results = {}
        ids_with_tags = Resource.objects.approved(
            user=user,
        ).exclude(
            id=self.id,
        ).values_list(
            'id',
            'tags',
        )
        for resource_id, tag in ids_with_tags:
            if resource_id in data:
                data[resource_id].append(tag)
            else:
                data[resource_id] = [tag]
        resource_tags = set(self.tags.values_list('id', flat=True))

        for resource_id, tags in data.items():
            matches = set(tags) & resource_tags
            results[resource_id] = len(matches)

        resources_ids = sorted(results, key=results.get, reverse=True)[:limit]
        preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(resources_ids)])
        resources = Resource.objects.filter(id__in=resources_ids).order_by(preserved)
        return resources


class ResourceCategory(models.Model):
    title = models.CharField(max_length=64, unique=True)
    slug = models.SlugField(max_length=64, unique=True)
    description = models.TextField()
    image = ImageField(
        'Lead category image',
        upload_to='uploads/resources/categories/images/%Y/%m/%d',
    )

    class Meta:
        ordering = ('title',)
        verbose_name_plural = 'Resource categories'

    def __str__(self):
        return self.title

    def get_resource_count(self, user=None):
        return self.resource_set.approved(user).count()

    get_resource_count.verbose_name = 'Resources'

    def get_absolute_url(self):
        return reverse('resources:resource-category-detail', kwargs={'slug': self.slug})

    def get_approved_featured_resources(self, user):
        categories_featured_resources = self.category_featured_resources.values_list('resource_id')

        return Resource.objects.approved(user).filter(id__in=categories_featured_resources)


class ResourceCategoryFeatured(SortableMixin):
    category = models.ForeignKey(
        ResourceCategory, on_delete=models.CASCADE, related_name='category_featured_resources'
    )
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE)
    project_order = models.PositiveIntegerField(default=0, editable=False, db_index=True)

    class Meta:
        verbose_name = 'Featured Resource'
        ordering = ['project_order']

    def __str__(self):
        return self.resource.title

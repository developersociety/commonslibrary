from django.conf import settings
from django.db import models

from ckeditor.fields import RichTextField
from mptt.models import MPTTModel

from .validators import validate_page_url


class Category(MPTTModel):
    title = models.CharField(max_length=64, unique=True)
    slug = models.SlugField(max_length=64, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ('id',)

    def __str__(self):
        return self.title


class Page(models.Model):
    title = models.CharField(max_length=256)
    content = RichTextField(
        blank=True,
    )
    author = models.CharField(max_length=256, blank=True)
    url = models.CharField(max_length=128, db_index=True, validators=[validate_page_url])
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='pages_created'
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='pages_updated'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('id',)

    def __str__(self):
        return "{url} -- {title}".format(url=self.url, title=self.title)

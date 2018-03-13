from django.db import models

from mptt.models import MPTTModel, TreeForeignKey


class Tag(MPTTModel):
    title = models.CharField(max_length=64, unique=True)
    slug = models.SlugField(max_length=64, unique=True)
    parent = TreeForeignKey(
        'self',
        null=True,
        blank=True,
        related_name='children',
        db_index=True,
        limit_choices_to=models.Q(level=0) | models.Q(level=1)
    )

    def __str__(self):
        return self.title

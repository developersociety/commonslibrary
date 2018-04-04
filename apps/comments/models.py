from django.conf import settings
from django.db import models
from django.utils import timezone

from resources.models import Resource


class Comment(models.Model):
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE)
    body = models.TextField()
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return '{user} - {created_at}'.format(user=self.created_by, created_at=self.created_at)


class Report(models.Model):
    body = models.TextField()
    comment = models.ForeignKey(Comment)
    reviewed = models.BooleanField(default=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)

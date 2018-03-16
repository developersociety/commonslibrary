from django.db import models


class ResourceManager(models.Manager):

    def approved(self, user=None):
        return self.filter(is_approved=True)

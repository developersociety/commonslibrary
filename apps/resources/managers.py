from django.db import models
from django.db.models import Q

from .choices import RESOURCE_APPROVED


class ResourceManager(models.Manager):

    def approved(self, user=None):
        if user:
            if user.is_authenticated:
                if user.is_superuser:
                    qs = self.filter(status=RESOURCE_APPROVED)
                else:
                    qs = self.filter(status=RESOURCE_APPROVED).filter(
                        Q(privacy__isnull=True) | Q(privacy__in=user.approved_organisations.all())
                    ).distinct()
            else:
                qs = self.filter(status=RESOURCE_APPROVED, privacy__isnull=True)
        else:
            qs = self.filter(status=RESOURCE_APPROVED, privacy__isnull=True)
        return qs

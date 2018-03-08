from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.postgres.fields import CIEmailField
from django.db import models
from django.utils import timezone

from sorl.thumbnail import ImageField

from directory.models import Organisation

from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    email = CIEmailField('email address', unique=True)
    first_name = models.CharField('first name', max_length=30)
    is_email_confirmed = models.BooleanField(default=False)
    first_name = models.CharField('first name', max_length=30)
    last_name = models.CharField('last name', max_length=30)
    is_staff = models.BooleanField(
        'staff status',
        default=False,
        help_text='Designates whether the user can log into this admin site.'
    )
    is_active = models.BooleanField(
        'active',
        default=False,
        help_text=(
            'Designates whether this user should be treated as '
            'active. Unselect this instead of deleting accounts.'
        )
    )
    date_joined = models.DateTimeField('date joined', default=timezone.now)
    photo = ImageField('Profile picture', upload_to='uploads/accounts/images/%Y/%m/%d', blank=True)
    phone = models.CharField('Phone Number', max_length=32, blank=True)
    address = models.TextField('Work address', blank=True)
    organisations = models.ManyToManyField(Organisation, blank=True)
    address = models.TextField('Work address', blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('first_name', 'last_name',)

    class Meta:
        db_table = 'auth_user'

    def __str__(self):
        return self.email

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """
        Returns the short name for the user.
        """
        return self.first_name

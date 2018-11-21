from django.contrib import admin

from rest_framework.authtoken.admin import TokenAdmin as BaseTokenAdmin
from rest_framework.authtoken.models import Token

admin.site.unregister(Token)


@admin.register(Token)
class TokenAdmin(BaseTokenAdmin):
    raw_id_fields = ('user',)
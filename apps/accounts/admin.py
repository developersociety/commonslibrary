from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

from .forms import UserCreationForm
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'is_staff', 'is_superuser',)
    ordering = ('-date_joined',)
    add_form = UserCreationForm
    filter_horizontal = ('organisations',)
    add_fieldsets = [
        (
            'User', {
                'classes': ('wide',),
                'fields': ('email', 'first_name', 'last_name', 'password1', 'password2'),
            }
        ),
    ]
    fieldsets = [
        ('User', {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'photo', 'phone', 'address',)}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser',)}),
        ('Organisations', {'fields': ('organisations',)}),
        ('Important dates', {'fields': ('last_login', 'date_joined'), 'classes': ('collapse',)}),
    ]

    def response_change(self, request, obj):
        """ Add permission to the users if it's set to staff and belongs to the organisation. """
        response = super().response_change(request, obj)
        self.add_remove_permissions(obj)
        return response

    def get_queryset(self, request):
        """ Only display users which belongs for the requested user. """
        qs = super().get_queryset(request)
        if not request.user.is_superuser and request.user.organisations.exists():
            qs = qs.filter(organisations__in=request.user.organisations.all()).distinct()
        return qs

    def add_remove_permissions(self, obj):
        if obj.is_staff:
            content_type = ContentType.objects.get_for_model(User)
            try:
                permission = Permission.objects.get(
                    content_type=content_type, codename='change_user'
                )
            except Permission.DoesNotExist:
                pass
            else:
                if obj.organisations.exists():
                    obj.user_permissions.add(permission)
                else:
                    permission_string = '{app_label}.{permission}'.format(
                        app_label=permission.content_type.app_label,
                        permission=permission.codename,
                    )
                    if obj.has_perm(permission_string):
                        obj.user_permissions.remove(permission)

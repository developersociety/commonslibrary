from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q

from .forms import UserChangeForm, UserCreationForm
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    list_display = ('email', 'first_name', 'last_name', 'is_staff', 'is_superuser',)
    ordering = ('-date_joined',)
    add_form = UserCreationForm
    filter_horizontal = ('chosen_organisations', 'approved_organisations',)
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
        ('Chosen Organisations', {'fields': ('chosen_organisations',)}),
        (
            'Approved Organisations',
            {'fields': ('approved_organisations',), 'classes': ('collase',)}
        ),
        ('Important dates', {'fields': ('last_login', 'date_joined'), 'classes': ('collapse',)}),
    ]

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = ['chosen_organisations']
        if obj is not None and obj.is_staff:
            readonly_fields.append('approved_organisations')
        return readonly_fields

    def response_change(self, request, obj):
        """ Add permission to the users if it's set to staff and belongs to the organisation. """
        response = super().response_change(request, obj)

        if obj.is_staff and not obj.is_superuser:
            self.add_remove_permissions(obj)

        return response

    def get_queryset(self, request):
        """ Only display users which belongs for the requested user. """
        qs = super().get_queryset(request)
        if not request.user.is_superuser and request.user.approved_organisations.exists():
            qs = qs.filter(
                Q(chosen_organisations__in=request.user.approved_organisations.all()) |
                Q(approved_organisations__in=request.user.approved_organisations.all())
            ).exclude(is_superuser=True).distinct()
        return qs

    def add_remove_permissions(self, obj):
        content_type = ContentType.objects.get_for_model(User)
        try:
            permission = Permission.objects.get(content_type=content_type, codename='change_user')
        except Permission.DoesNotExist:
            pass
        else:
            if obj.approved_organisations.exists():
                obj.user_permissions.add(permission)
            else:
                permission_string = '{app_label}.{permission}'.format(
                    app_label=permission.content_type.app_label,
                    permission=permission.codename,
                )
                if obj.has_perm(permission_string):
                    obj.user_permissions.remove(permission)

    def get_form(self, request, obj=None, **kwargs):
        """ Assign request to the form. """
        form = super().get_form(request=request, obj=obj, **kwargs)
        form.request = request
        return form

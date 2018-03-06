from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .forms import UserCreationForm
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'is_staff', 'is_superuser',)
    ordering = ('-date_joined',)
    add_form = UserCreationForm
    add_fieldsets = [
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'password1', 'password2'),
        }),
    ]
    fieldsets = [
        ('User', {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'photo', 'phone', 'address',)}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', )}),
        ('Important dates', {'fields': ('last_login', 'date_joined'), 'classes': ('collapse',)}),
    ]

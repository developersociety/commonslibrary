from django.contrib import admin

from django_mptt_admin.admin import DjangoMpttAdmin

from .models import Tag


@admin.register(Tag)
class TagsAdmin(DjangoMpttAdmin):
    list_display = ('title', 'slug', 'parent',)
    readonly_fields = ('id',)
    search_fields = ['title']
    prepopulated_fields = {'slug': ('title',)}
    fieldsets = [
        ('Tag', {
            'fields': ('title', 'slug', 'parent'),
        }),
        ('Meta', {
            'classes': ('collapse',),
            'fields': ('id',),
        }),
    ]

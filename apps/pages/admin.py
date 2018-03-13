from django.contrib import admin

from django_mptt_admin.admin import DjangoMpttAdmin
from mptt.admin import MPTTModelAdmin

from .models import Category, Page


@admin.register(Category)
class CategoryAdmin(DjangoMpttAdmin, MPTTModelAdmin):
    list_display = ('title',)
    search_fields = ['title']
    prepopulated_fields = {'slug': ('title',)}
    fieldsets = [
        ('Category', {
            'fields': ('title', 'slug', 'description',),
        }),
    ]
    mptt_level_indent = 25


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'created_by', 'created_at',)
    list_filter = ('category',)
    readonly_fields = ('id', 'created_by', 'updated_by',)
    search_fields = ['title', 'content', 'author']
    date_hierarchy = 'created_at'
    fieldsets = [
        ('Page', {
            'fields': ('title', 'url', 'category', 'author',),
        }),
        ('Content', {
            'fields': ('content',),
        }),
        ('Meta', {
            'classes': ('collapse',),
            'fields': ('id', 'created_by', 'updated_by'),
        }),
    ]

    def save_model(self, request, obj, form, change):
        """ Assign user to the object created_by and updated_by. """
        if obj.id and change:
            obj.updated_by = request.user
        if not obj.id:
            obj.created_by = request.user
            obj.updated_by = request.user
        super().save_model(request, obj, form, change)

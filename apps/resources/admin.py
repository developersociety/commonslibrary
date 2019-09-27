from django.contrib import admin

from . import models


class ResourceCategoryFeaturedInline(admin.TabularInline):
    model = models.ResourceCategoryFeatured


@admin.register(models.ResourceCategory)
class ResourceCategoryAdmin(admin.ModelAdmin):
    list_display = ('title',)
    inlines = [
        ResourceCategoryFeaturedInline
    ]



@admin.register(models.Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'abstract', 'hits', 'created_by', 'created_at')
    list_editable = ('status',)
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ('tags', 'privacy')
    search_fields = ['title', 'abstract']
    date_hierarchy = 'created_at'
    fieldsets = [
        ('Resource', {
            'fields': ('title', 'slug', 'abstract', 'tags', 'status'),
        }),
        ('Content', {
            'fields': ('content', 'image'),
        }),
        ('Privacy and Organisation', {
            'fields': ('privacy', 'organisation'),
        }),
        ('Counts', {
            'fields': ('likes', 'tried', 'hits'),
        }),
        (
            'Meta', {
                'classes': ('collapse',),
                'fields': ('id', 'updated_by', 'created_by', 'updated_at', 'created_at'),
            }
        ),
    ]

    def has_add_permission(self, request):
        return False

    def get_queryset(self, request):
        """ Only display resources which belongs for the requested user. """
        qs = super().get_queryset(request)
        if not request.user.is_superuser and request.user.approved_organisations.exists():
            qs = qs.filter(organisation__in=request.user.approved_organisations.all()).distinct()
        return qs

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = [
            'abstract', 'id', 'created_by', 'updated_by', 'created_at', 'updated_at', 'likes',
            'tried', 'hits', 'organisation', 'tags'
        ]
        user = request.user
        if obj.organisation not in user.approved_organisations.all():
            readonly_fields.append('privacy')
        return readonly_fields

    def get_list_filter(self, request):
        """
        Returns a sequence containing the fields to be displayed as filters in
        the right sidebar of the changelist page.
        """
        list_filter = ['status', 'tags']
        if request.user.is_superuser:
            list_filter.append('organisation')
        return list_filter

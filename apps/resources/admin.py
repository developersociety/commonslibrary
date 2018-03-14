from django.contrib import admin

from .models import Resource


@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ('title', 'abstract', 'likes', 'tried', 'hits', 'created_by', 'created_at')
    readonly_fields = (
        'abstract', 'id', 'created_by', 'updated_by', 'created_at', 'updated_at', 'likes', 'tried',
        'hits', 'privacy', 'organisation', 'tags', 'image',
    )
    filter_horizontal = ('tags', 'privacy')
    search_fields = ['title', 'abstract', 'created_by', 'updated_by']
    date_hierarchy = 'created_at'
    fieldsets = [
        ('Resource', {
            'fields': ('title', 'abstract', 'tags', 'is_approved'),
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
        ('Meta', {
            'classes': ('collapse',),
            'fields': ('id', 'updated_by', 'created_by', 'updated_at', 'created_at'),
        }),
    ]

    def has_add_permission(self, request):
        return False

    def get_queryset(self, request):
        """ Only display resources which belongs for the requested user. """
        qs = super().get_queryset(request)
        if not request.user.is_superuser and request.user.approved_organisations.exists():
            qs = qs.filter(organisation__in=request.user.approved_organisations.all()).distinct()
        return qs

    def get_list_filter(self, request):
        """
        Returns a sequence containing the fields to be displayed as filters in
        the right sidebar of the changelist page.
        """
        list_filter = ['is_approved', 'tags']
        if request.user.is_superuser:
            list_filter.append('organisation')
        return list_filter

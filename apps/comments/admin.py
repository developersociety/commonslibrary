from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from .models import Comment, Report


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('created_by', 'body',)

    def has_add_permission(self, request):
        return False

    def get_readonly_fields(self, request, obj=None):
        fields = [field.name for field in self.model._meta.fields]
        return fields


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('id', 'reviewed', 'comment', 'created_by', 'created_at',)
    list_filter = ('reviewed',)
    fieldsets = [
        (
            'Report', {
                'fields': (
                    'body', 'get_abused_comment', 'get_comment_url', 'get_resource_url',
                    'reviewed',
                )
            }
        ),
        ('Meta', {'classes': ('collapse',), 'fields': ('id', 'created_by', 'created_at',)}),
    ]

    def has_add_permission(self, request):
        return False

    def get_readonly_fields(self, request, obj=None):
        fields = [field.name for field in self.model._meta.fields if field.name != 'reviewed']
        fields += ['get_resource_url', 'get_comment_url', 'get_abused_comment']
        return fields

    def get_resource_url(self, obj):
        return format_html(
            '<a href="{url}" target="_blank">Resource URL</a>'.format(
                url=obj.comment.resource.get_absolute_url(),
            )
        )

    get_resource_url.short_description = 'Resource URL'

    def get_comment_url(self, obj):
        return format_html(
            '<a href="{url}" target="_blank">Comment URL</a>'.format(
                url=reverse('admin:comments_comment_change', args=(obj.comment.id,)),
            )
        )

    get_comment_url.short_description = 'Comment URL'

    def get_abused_comment(self, obj):
        return obj.comment.body

    get_abused_comment.short_description = 'Abused comment text'

    def get_queryset(self, request):
        """ Only display resources which belongs for the requested user. """
        qs = super().get_queryset(request)
        if not request.user.is_superuser and request.user.approved_organisations.exists():
            qs = qs.filter(
                comment__resource__organisation__in=request.user.approved_organisations.all()
            ).distinct()
        return qs

from django.contrib import admin, messages
from django.shortcuts import render
from django.urls import reverse
from django.utils.html import mark_safe

from adminsortable.admin import NonSortableParentAdmin, SortableStackedInline

from . import models


class ResourceCategoryFeaturedInline(SortableStackedInline):
    model = models.ResourceCategoryFeatured

    def get_formset(self, request, obj=None, **kwargs):
        """
        Change order by title for the resource field
        """
        formset = super().get_formset(request, obj, **kwargs)
        resource_field = formset.form.base_fields['resource']
        resource_field.queryset = resource_field.queryset.order_by('title')
        return formset


@admin.register(models.ResourceCategory)
class ResourceCategoryAdmin(NonSortableParentAdmin):
    list_display = ('title', 'approved_resources', 'all_resources', 'admin_list_resources')
    prepopulated_fields = {'slug': ('title',)}
    extra = 1
    inlines = [ResourceCategoryFeaturedInline]

    def approved_resources(self, obj):
        return obj.get_resource_count()

    def all_resources(self, obj):
        return obj.resource_set.all().count()

    def admin_list_resources(self, obj):
        url = reverse('admin:resources_resource_changelist'
                      ) + '?categories__id__exact={}'.format(obj.id)
        return mark_safe('<a href="{}">{} Resources</a>'.format(url, obj.title))


@admin.register(models.Resource)
class ResourceAdmin(admin.ModelAdmin):
    actions = ['action_categorise']
    list_display = (
        'title', 'status', 'abstract', 'hits', 'created_by', 'created_at', 'categories_list'
    )
    list_editable = ('status',)
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ('tags', 'privacy')
    search_fields = ['title', 'abstract']
    date_hierarchy = 'created_at'

    fieldsets = [
        ('Resource', {
            'fields': ('title', 'slug', 'abstract', 'categories', 'tags', 'status'),
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
        list_filter = ['status', 'categories', 'tags']
        if request.user.is_superuser:
            list_filter.append('organisation')

        return list_filter

    def categories_list(self, obj):
        return ', '.join(obj.categories.all().values_list('title', flat=True))

    categories_list.short_description = 'Categories'

    def action_categorise(self, request, queryset):
        template = 'resources/admin/categorise_resources.html'

        ids = ','.join(str(pk) for pk in queryset.values_list('pk', flat=True))
        categories = models.ResourceCategory.objects.all()

        messages.info(request, '{} resources selected'.format(queryset.count()))

        return render(
            request, template, {
                "title": "Categorise Resources",
                "site_title": admin.site.site_title,
                "site_header": admin.site.site_header,
                "categories": categories,
                "resource_ids": ids,
                "post_to": reverse('resources:admin-categorise-resources'),
            }
        )

    action_categorise.short_description = 'Categorise selected resources'
    action_categorise.allowed_permissions = ('change',)

from django.contrib import admin

from .models import Organisation


@admin.register(Organisation)
class OrganisationAdmin(admin.ModelAdmin):
    list_display = ('title', 'url', 'telephone', 'email', 'created_by', 'created_at',)
    readonly_fields = ('id', 'created_by', 'updated_by', 'created_at', 'updated_at',)
    search_fields = ['title']
    date_hierarchy = 'created_at'
    fieldsets = [
        ('Organisation', {
            'fields': ('title', 'url', 'email', 'telephone', 'logo',),
        }),
        ('Texts', {
            'fields': ('address', 'description',),
        }),
        (
            'Meta', {
                'classes': ('collapse',),
                'fields': ('id', 'created_by', 'updated_by', 'created_at', 'updated_at',),
            }
        ),
    ]

    def save_model(self, request, obj, form, change):
        """ Assign user to the object created_by and updated_by. """
        if obj.id and change:
            obj.updated_by = request.user
        if not obj.id:
            obj.created_by = request.user
            obj.updated_by = request.user
        super().save_model(request, obj, form, change)
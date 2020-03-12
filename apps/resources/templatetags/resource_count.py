from django.template import Library
from django.template.defaulttags import cycle as cycle_original

register = Library()


@register.assignment_tag
def resource_count(resource_category, user):
    '''
    Provide a count of available resources for a category depending on
    the user
    '''
    return resource_category.get_resource_count(user)

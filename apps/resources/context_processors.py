from .models import ResourceCategory


def resource_categories(request):
    """
    Add categories for categories drop down
    """
    return {'resources_categories': ResourceCategory.objects.all()}

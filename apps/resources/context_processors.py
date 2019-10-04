from .models import ResourceCategory


def resource_categories(request):
    """
    Add categories for explore drop down
    """
    return {'resources_categories': ResourceCategory.objects.all()}

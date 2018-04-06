from .models import Organisation


def footer_orgs(request):
    return {'footer_orgs': Organisation.objects.all()}

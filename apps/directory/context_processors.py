from .models import Organisation


def footer_orgs(request):
    return {
        'footer_orgs_founders': Organisation.objects.filter(founder=True).order_by('title'),
        'footer_orgs_partners': Organisation.objects.filter(founder=False).order_by('title'),
    }

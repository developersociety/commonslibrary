from .models import Organisation


def footer_orgs(request):
    return {
        'footer_orgs_founders': Organisation.objects.filter(founder=True, show_logo_on_footer=True).order_by('title'),
        'footer_orgs_partners': Organisation.objects.filter(founder=False, show_logo_on_footer=True).order_by('title'),
    }

from django.core.exceptions import ValidationError


def validate_page_url(value):
    if not value.startswith('/'):
        raise ValidationError('URL must start with a /')

    if not value.endswith('/'):
        raise ValidationError('URL must end with a /')

    if value.startswith('//'):
        raise ValidationError('Protocol relative URLs are not allowed')

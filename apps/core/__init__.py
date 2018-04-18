from django.forms.fields import CharField

from PIL import ImageFile

from .validators import ProhibitNullCharactersValidator

ImageFile.LOAD_TRUNCATED_IMAGES = True

# Make CharField form field prohibit null characters
CharField.default_validators.append(ProhibitNullCharactersValidator())

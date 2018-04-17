import ntpath

from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from django.utils.text import slugify

import requests
from import_export import fields, resources

from tags.models import Tag

from .models import Resource
from .widgets import TagsManyToManyWidget


class ResourceResource(resources.ModelResource):

    tags = fields.Field(
        column_name='tags',
        attribute='tags',
        widget=TagsManyToManyWidget(model=Tag, field='title')
    )

    class Meta:
        model = Resource
        fields = (
            'id', 'title', 'abstract', 'content', 'image', 'tags', 'organisation', 'privacy',
            'status', 'created_by', 'updated_by',
        )

    def get_instance(self, instance_loader, row):
        return False

    def before_save_instance(self, instance, using_transactions, dry_run):
        response = requests.get(instance.image.name)
        data = response.content
        img_temp = NamedTemporaryFile(delete=True)
        img_temp.write(data)
        img_temp.flush()

        image_file = File(img_temp)
        file_name = ntpath.basename(instance.image.name)

        instance.image.save(file_name, image_file)
        image_file.close()

        instance.slug = slugify(instance.title)
        instance.updated_by = instance.created_by

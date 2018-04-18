import csv
import ntpath
import re

from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from django.core.management.base import BaseCommand
from django.utils.text import slugify

import requests
from resources.imports import ResourceCSVRow
from resources.models import Resource
from tags.models import Tag


class Command(BaseCommand):
    help = 'Import resources'

    def add_arguments(self, parser):
        parser.add_argument('file', nargs="?", help='csv file location.')

    def handle(self, *args, **options):
        Resource.objects.all().delete()
        with open(options['file'], 'r') as csv_file:
            csv_file = csv.reader(csv_file, delimiter=',')
            next(csv_file, None)

            for line in csv_file:
                data = ResourceCSVRow._make(line)

                content = self.sanitize_content(data.content)
                slug = slugify(data.title)

                image = None
                if data.image:
                    image = self.get_image(data.image)

                tags_ids = []
                tags = data.tags.split(',')
                tags = [tag.title().strip() for tag in tags]
                for tag in tags:
                    if not Tag.objects.filter(title=tag).exists():
                        slug = slugify(tag)
                        tag = Tag.objects.create(title=tag, slug=slug)
                    else:
                        tag = Tag.objects.get(title=tag)
                    tags_ids.append(tag.id)

                privacy_ids = None
                if data.privacy:
                    privacy_ids = data.privacy.split(',')

                resource = Resource.objects.create(
                    title=data.title,
                    slug=slug,
                    abstract=data.abstract,
                    content=content,
                    organisation_id=data.organisation,
                    status=data.status,
                    created_by_id=data.created_by,
                    updated_by_id=data.created_by,
                )
                resource.tags.add(*tags_ids)

                if privacy_ids:
                    resource.privacy.add(*privacy_ids)

                if image:
                    resource.image.save(*image)

    def get_image(self, url):
        response = requests.get(url)
        data = response.content

        img_temp = NamedTemporaryFile(delete=True)
        img_temp.write(data)
        img_temp.flush()

        image_file = File(img_temp)
        file_name = ntpath.basename(url)
        return (file_name, image_file)

    def sanitize_content(self, content):
        remove_words = [
            '[vc_row]', '[vc_column]', '[vc_column_text]', '[/vc_column_text]', '[/vc_column]',
            '[/vc_row]'
        ]
        for word in remove_words:
            content = content.replace(word, '')

        # Replace accordion [vc_tta_accordion active_section="0" collapsible_all="true"]
        content = re.sub('\[vc_tta_acc(.*?)]', '<ul class="mj_accordion">', content)
        content = re.sub('\[/vc_tta_acc(.*?)]', '</ul>', content)

        counter = 0
        # Get accordion titles
        accordion_titles = re.findall('subject line: (.*?)"', content)

        html_content = """
            <li>
            <div class="mj_accordion_item {css_class}">{title}</div>
            <div class="mj_accordion_content {css_class}">
        """
        # Loop through accordion title and relace vs with our accordion.
        for title in accordion_titles:
            css_class = ''
            if counter == 0:
                css_class = 'active'

            content = re.sub(
                '\[vc_tta_sec(.*?)]',
                html_content.format(css_class=css_class, title=title),
                content,
                1,
            )
            content = re.sub('\[/vc_tta_sec(.*?)]', '</div></li>', content, 1)

        return content

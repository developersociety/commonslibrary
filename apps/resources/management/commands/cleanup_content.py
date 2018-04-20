import re

from django.core.management.base import BaseCommand

from resources.models import Resource


class Command(BaseCommand):
    help = 'Cleanup imported resources'

    def add_arguments(self, parser):
        parser.add_argument('file', nargs="?", help='csv file location.')

    def handle(self, *args, **options):
        html_content = """
            <li>
            <div class="mj_accordion_item {css_class}">{title}</div>
            <div class="mj_accordion_content {css_class}">
        """
        for resource in Resource.objects.all():
            if '[vc_tta_section title' in resource.content:
                accordion_titles = re.findall('\[vc_tta_section title=.(.*?)"', resource.content)
                counter = 0
                for title in accordion_titles:
                    css_class = ''
                    if counter == 0:
                        css_class = 'active'

                    content = re.sub(
                        '\[vc_tta_sec(.*?)]',
                        html_content.format(css_class=css_class, title=title),
                        resource.content,
                        1,
                    )
                    content = re.sub('\[/vc_tta_sec(.*?)]', '</div></li>', content, 1)
                    resource.content = content
                    resource.save()

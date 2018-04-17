from django.utils.text import slugify

from import_export.widgets import ManyToManyWidget as BaseManyToManyWidget


class TagsManyToManyWidget(BaseManyToManyWidget):

    def clean(self, value, row=None, *args, **kwargs):
        ids = value.split(self.separator)
        ids = [i.title().strip() for i in ids]
        for tag in ids:
            if not self.model.objects.filter(title=tag).exists():
                slug = slugify(tag)
                self.model.objects.create(title=tag, slug=slug)
        return self.model.objects.filter(**{'%s__in' % self.field: ids})

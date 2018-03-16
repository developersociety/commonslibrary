from django.utils.text import slugify

import factory

from tags.models import Tag


class TagFactory(factory.django.DjangoModelFactory):
    title = factory.Faker('job')
    slug = factory.LazyAttribute(lambda a: slugify(a.title))

    class Meta:
        model = Tag

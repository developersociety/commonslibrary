from django.utils.text import slugify

import factory

from tags.models import Tag


class TagFactory(factory.django.DjangoModelFactory):
    title = factory.Sequence(lambda n: '{id}{job}'.format(id=n, job=factory.Faker('job')))
    slug = factory.LazyAttribute(lambda a: slugify(a.title))

    class Meta:
        model = Tag

from django.utils.text import slugify

import factory

from accounts.tests.factories import UserFactory
from pages.models import Category, Page


class CategoryFactory(factory.django.DjangoModelFactory):
    title = factory.Faker('job')
    slug = factory.LazyAttribute(lambda a: slugify(a.title))

    class Meta:
        model = Category


class PageFactory(factory.django.DjangoModelFactory):
    title = factory.Faker('job')
    url = factory.LazyAttribute(lambda a: '/{slug}/'.format(slug=slugify(a.title)))
    category = factory.SubFactory(CategoryFactory)
    created_by = factory.SubFactory(UserFactory)
    updated_by = factory.LazyAttribute(lambda a: a.created_by)

    class Meta:
        model = Page

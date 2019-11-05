from django.utils.text import slugify

import factory

from accounts.tests.factories import UserFactory
from directory.tests.factories import OrganisationFactory
from resources.models import Resource, ResourceCategory, ResourceCategoryFeatured


class ResourceCategoryFactory(factory.django.DjangoModelFactory):
    title = factory.Sequence(lambda n: '{id}'.format(id=n))
    slug = factory.LazyAttribute(lambda a: slugify(a.title))
    description = factory.Faker('job')

    class Meta:
        model = ResourceCategory


class ResourceFactory(factory.django.DjangoModelFactory):
    title = factory.Sequence(lambda n: '{id}'.format(id=n))
    slug = factory.LazyAttribute(lambda a: slugify(a.title))
    abstract = factory.Faker('job')
    content = factory.Faker('job')
    organisation = factory.SubFactory(OrganisationFactory)
    created_by = factory.SubFactory(UserFactory)
    updated_by = factory.SubFactory(UserFactory)

    class Meta:
        model = Resource

    @factory.post_generation
    def tags(self, created, extracted, **kwargs):
        if not created:
            return
        if extracted:
            for tag in extracted:
                self.tags.add(tag)

    @factory.post_generation
    def privacy(self, created, extracted, **kwargs):
        if not created:
            return
        if extracted:
            for privacy in extracted:
                self.privacy.add(privacy)

    @factory.post_generation
    def tried(self, created, extracted, **kwargs):
        if not created:
            return
        if extracted:
            for user in extracted:
                self.tried.add(user)

    @factory.post_generation
    def likes(self, created, extracted, **kwargs):
        if not created:
            return
        if extracted:
            for user in extracted:
                self.likes.add(user)


class ResourceCategoryFeaturedFactory(factory.django.DjangoModelFactory):
    category = factory.SubFactory(ResourceCategoryFactory)
    resource = factory.SubFactory(ResourceFactory)

    class Meta:
        model = ResourceCategoryFeatured

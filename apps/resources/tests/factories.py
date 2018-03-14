import factory

from accounts.tests.factories import UserFactory
from directory.tests.factories import OrganisationFactory
from resources.models import Resource


class ResourceFactory(factory.django.DjangoModelFactory):
    title = factory.Sequence(lambda n: '{id}{job}'.format(id=n, job=factory.Faker('job')))
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
                self.privarcy.add(privacy)

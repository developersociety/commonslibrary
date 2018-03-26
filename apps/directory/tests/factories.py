import factory

from accounts.tests.factories import UserFactory
from directory.models import Organisation


class OrganisationFactory(factory.django.DjangoModelFactory):
    title = factory.Sequence(lambda n: '{id}{job}'.format(id=n, job=factory.Faker('job')))
    created_by = factory.SubFactory(UserFactory)
    updated_by = factory.LazyAttribute(lambda a: a.created_by)

    class Meta:
        model = Organisation

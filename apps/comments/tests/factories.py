import factory

from accounts.tests.factories import UserFactory
from comments.models import Comment
from resources.tests.factories import ResourceFactory


class CommentFactory(factory.django.DjangoModelFactory):
    resource = factory.SubFactory(ResourceFactory)
    body = factory.Faker('job')
    created_by = factory.SubFactory(UserFactory)

    class Meta:
        model = Comment

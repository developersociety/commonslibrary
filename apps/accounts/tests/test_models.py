from django.test import TestCase

from resources.choices import RESOURCE_APPROVED
from resources.tests.factories import ResourceFactory

from .factories import UserFactory


class UserTest(TestCase):

    def setUp(self):
        self.resource_most_tried = ResourceFactory.create(
            tried=[UserFactory.create(), UserFactory.create()],
            status=RESOURCE_APPROVED,
        )
        self.resource_most_liked = ResourceFactory.create(
            likes=[UserFactory.create(), UserFactory.create(), UserFactory.create()],
            status=RESOURCE_APPROVED,
        )
        self.user = UserFactory.create()

    def test_create(self):
        obj = UserFactory.create()
        self.assertIsNotNone(obj.id)

    def test_get_most_tried_resource(self):
        resource = ResourceFactory.create(
            tried=[self.user, UserFactory.create()],
            status=RESOURCE_APPROVED,
        )
        self.assertEqual(self.user.get_most_tried_resource().id, resource.id)

    def test_get_most_liked_resource(self):
        resource = ResourceFactory.create(
            likes=[self.user, UserFactory.create()],
            status=RESOURCE_APPROVED,
        )
        self.assertEqual(self.user.get_most_liked_resource().id, resource.id)

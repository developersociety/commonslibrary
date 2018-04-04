from django.test import TestCase

from accounts.tests.factories import UserFactory
from resources.models import Resource
from resources.tests.factories import ResourceFactory


class ResourceModelTestCase(TestCase):

    def test_get_carousel_resources(self):
        ResourceFactory.create(
            title='first', likes=UserFactory.create_batch(size=10), is_approved=True
        )
        second = ResourceFactory.create(
            title='second', tried=UserFactory.create_batch(size=5), hits=20, is_approved=True
        )
        resources = Resource.get_carousel_resources(limit=1)
        self.assertIn(second, resources)

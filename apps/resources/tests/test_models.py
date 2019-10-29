from django.test import TestCase

from accounts.tests.factories import UserFactory
from resources.choices import RESOURCE_APPROVED
from resources.models import Resource
from resources.tests.factories import ResourceFactory
from tags.tests.factories import TagFactory

from .factories import ResourceCategoryFeaturedFactory


class ResourceModelTestCase(TestCase):

    def test_get_carousel_resources(self):
        ResourceFactory.create(
            title='first', likes=UserFactory.create_batch(size=10), status=RESOURCE_APPROVED
        )
        second = ResourceFactory.create(
            title='second',
            tried=UserFactory.create_batch(size=5),
            hits=20,
            status=RESOURCE_APPROVED,
        )
        resources = Resource.get_carousel_resources(limit=1)
        self.assertIn(second, resources)

    def test_get_related_resources(self):
        resource = ResourceFactory.create(
            status=RESOURCE_APPROVED, tags=TagFactory.create_batch(10)
        )
        tag = resource.tags.all()[0]
        tag_1 = resource.tags.all()[1]
        tag_2 = resource.tags.all()[2]
        resource_2 = ResourceFactory.create(status=RESOURCE_APPROVED, tags=[tag])
        resource_3 = ResourceFactory.create(status=RESOURCE_APPROVED, tags=[tag_1, tag_2])
        resource_4 = ResourceFactory.create(status=RESOURCE_APPROVED, tags=[tag, tag_1, tag_2])
        resources = resource.get_related()
        self.assertEqual(resource_4.id, resources[0].id)
        self.assertEqual(resource_3.id, resources[1].id)
        self.assertEqual(resource_2.id, resources[2].id)


class ResourceCategoryFeaturedTest(TestCase):

    def test_factory(self):
        obj = ResourceCategoryFeaturedFactory.create()
        self.assertIsNotNone(obj.id)

from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from accounts.tests.factories import UserFactory
from directory.tests.factories import OrganisationFactory
from resources.tests.factories import ResourceFactory
from tags.tests.factories import TagFactory


class ResourceTests(APITestCase):

    def setUp(self):
        self.url = reverse('resource-list')
        ResourceFactory.create(is_approved=True)
        ResourceFactory.create(is_approved=False)
        self.organisation = OrganisationFactory.create()
        self.user = UserFactory.create(
            is_staff=True, approved_organisations=[self.organisation], password='test123'
        )
        ResourceFactory.create(privacy=[self.organisation], is_approved=True)

    def test_get_list(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_list_with_privacy(self):
        client = APIClient()
        client.login(username=self.user.email, password='test123')
        response = client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)


class OrganisationTests(APITestCase):

    def setUp(self):
        OrganisationFactory.create()

    def test_get_list(self):
        url = reverse('organisation-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TagTests(APITestCase):

    def setUp(self):
        TagFactory.create()

    def test_get_list(self):
        url = reverse('tag-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

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
        self.resource_1 = ResourceFactory.create(is_approved=True)
        self.update_url = reverse('resource-detail', kwargs={'pk': self.resource_1.id})
        self.organisation = OrganisationFactory.create()
        self.user = UserFactory.create(
            is_staff=True, approved_organisations=[self.organisation], password='test123'
        )
        self.logged_in_client = APIClient()
        self.logged_in_client.login(username=self.user.email, password='test123')

        ResourceFactory.create(is_approved=False)
        ResourceFactory.create(privacy=[self.organisation], is_approved=True)

    def test_get_list(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_list_with_privacy(self):
        response = self.logged_in_client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_update_with_anonymous(self):
        response = self.client.put(self.update_url, {'like': 'true'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_likes_with_auth(self):
        response = self.logged_in_client.put(self.update_url, {'like': 'true'}, format='json')

        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        self.assertTrue(self.user in self.resource_1.likes.all())

        response = self.logged_in_client.put(self.update_url, {'like': 'false'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        self.assertFalse(self.user in self.resource_1.likes.all())

    def test_update_tries_with_auth(self):
        response = self.logged_in_client.put(self.update_url, {'tried': 'true'}, format='json')

        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        self.assertTrue(self.user in self.resource_1.tried.all())

        response = self.logged_in_client.put(self.update_url, {'tried': 'false'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        self.assertFalse(self.user in self.resource_1.tried.all())


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


class UserTests(APITestCase):

    def setUp(self):
        UserFactory.create()

    def test_get_list(self):
        url = reverse('user-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

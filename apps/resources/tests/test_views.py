from django.urls import reverse

from django_webtest import WebTest

from accounts.tests.factories import UserFactory
from directory.tests.factories import OrganisationFactory
from pages.tests.factories import PageFactory
from resources.choices import RESOURCE_APPROVED
from resources.models import Resource

from .factories import ResourceCategoryFactory, ResourceCategoryFeaturedFactory, ResourceFactory


class ResourceThankTestView(WebTest):

    def setUp(self):
        PageFactory.create(url='/resources/thank-you/')

    def test_view(self):
        response = self.app.get(reverse('resources:resource-thank-you'))
        self.assertEqual(response.status_code, 200)


class ResourceUpdateTestView(WebTest):

    def setUp(self):
        self.organisation = OrganisationFactory.create()
        self.resource_category = ResourceCategoryFactory.create()
        self.resource = ResourceFactory.create(
            status=RESOURCE_APPROVED,
            organisation=self.organisation,
        )
        self.user = UserFactory.create()

    def test_view_no_auth(self):
        response = self.app.get(
            reverse('resources:resource-update', kwargs={'slug': self.resource.slug})
        )
        self.assertEqual(response.status_code, 302)

    def test_view_with_auth_random(self):
        response = self.app.get(
            reverse('resources:resource-update', kwargs={'slug': self.resource.slug}),
            user=self.user,
            expect_errors=True,
        )
        self.assertEqual(response.status_code, 403)

    def test_view_with_auth(self):
        response = self.app.get(
            reverse('resources:resource-update', kwargs={'slug': self.resource.slug}),
            user=self.resource.created_by,
        )
        form = response.form
        self.assertEqual(response.status_code, 200)
        self.assertEqual(form.fields['title'][0].value, self.resource.title)

    def test_submit_form(self):
        self.resource.created_by.approved_organisations.add(self.organisation)
        response = self.app.get(
            reverse('resources:resource-update', kwargs={'slug': self.resource.slug}),
            user=self.resource.created_by,
        )
        form = response.form
        form['categories'] = self.resource_category
        form['abstract'] = 'testing'
        response = form.submit()
        self.resource.refresh_from_db()

        self.assertEqual(self.resource.abstract, 'testing')
        self.assertEqual(response.status_code, 302)


class ResourceCreateViewViewTest(WebTest):

    def setUp(self):
        self.user = UserFactory.create(
            approved_organisations=OrganisationFactory.create_batch(size=10)
        )
        self.resource_category = ResourceCategoryFactory.create()
        self.initial = {
            'title': 'test',
            'abstract': 'abstract',
            'content': 'content',
        }

    def test_view_no_auth(self):
        response = self.app.get(reverse('resources:resource-create'))
        self.assertEqual(response.status_code, 302)

    def test_view_public(self):
        response = self.app.get(reverse('resources:resource-create'), user=self.user)
        organisation = self.user.approved_organisations.all()[0]
        form = response.form
        for name, field in form.fields.items():
            if self.initial.get(name):
                field[0].value = self.initial[name]
        form['is_public'] = True
        form['categories'] = self.resource_category
        form['organisation'] = str(organisation.id)
        response = form.submit()

        resource = Resource.objects.get(title='test')

        self.assertEqual(response.status_code, 302)
        self.assertEqual(resource.organisation_id, organisation.id)
        self.assertFalse(resource.privacy.exists())

    def test_not_public(self):
        response = self.app.get(reverse('resources:resource-create'), user=self.user)
        organisation = self.user.approved_organisations.all()[0]
        form = response.form
        for name, field in form.fields.items():
            if self.initial.get(name):
                form[name].value = self.initial[name]
        form['is_public'] = False
        form['categories'] = self.resource_category
        form['organisation'] = str(organisation.id)
        response = form.submit()

        resource = Resource.objects.get(title='test')
        self.assertEqual(resource.privacy.count(), self.user.approved_organisations.count())


class ResourceDetailViewTest(WebTest):

    def test_resource_doesnot_exist(self):
        response = self.app.get(reverse('resources:resource-detail', kwargs={'slug': 'cat'}))
        self.assertEqual(response.location, reverse('home'))

    def test_resource_exist_no_access(self):
        organisation = OrganisationFactory.create()
        resource = ResourceFactory.create(
            slug='testing',
            status=RESOURCE_APPROVED,
            organisation=organisation,
            privacy=[organisation],
        )
        response = self.app.get(
            reverse('resources:resource-detail', kwargs={'slug': resource.slug})
        )
        url = '{url}?next={next}'.format(
            url=reverse('accounts:login'),
            next=resource.get_absolute_url(),
        )
        self.assertEqual(response.location, url)

    def test_resource_detail(self):
        organisation = OrganisationFactory.create()
        resource = ResourceFactory.create(
            slug='testing',
            status=RESOURCE_APPROVED,
            organisation=organisation,
            privacy=[organisation],
        )
        user = UserFactory.create(
            approved_organisations=[resource.organisation],
        )
        response = self.app.get(
            reverse('resources:resource-detail', kwargs={'slug': resource.slug}), user=user
        )
        self.assertEqual(response.status_code, 200)


class ResourceCategoryDetailView(WebTest):

    def setUp(self):
        self.organisation = OrganisationFactory.create()
        self.resource_category = ResourceCategoryFactory.create()

    def test_view_response(self):
        response = self.app.get(
            reverse(
                'resources:resource-category-detail', kwargs={'slug': self.resource_category.slug}
            ),
        )
        self.assertEqual(response.status_code, 200)

    def test_featured_resources_visible(self):
        resource = ResourceFactory.create(status=RESOURCE_APPROVED)
        ResourceCategoryFeaturedFactory.create(
            category=self.resource_category,
            resource=resource,
        )
        response = self.app.get(
            reverse(
                'resources:resource-category-detail', kwargs={'slug': self.resource_category.slug}
            )
        )
        featured_resources = response.context['featured_resources']
        self.assertTrue(featured_resources.exists())

    def test_featured_resources_not_visible(self):
        resource = ResourceFactory.create(
            status=RESOURCE_APPROVED,
            organisation=self.organisation,
            privacy=[self.organisation],
        )
        ResourceCategoryFeaturedFactory.create(
            category=self.resource_category,
            resource=resource,
        )
        response = self.app.get(
            reverse(
                'resources:resource-category-detail', kwargs={'slug': self.resource_category.slug}
            ),
        )
        featured_resources = response.context['featured_resources']
        self.assertFalse(featured_resources.exists())

    def test_featured_resources_visible_for_user(self):
        user = UserFactory.create(approved_organisations=[self.organisation])
        resource = ResourceFactory.create(
            status=RESOURCE_APPROVED,
            organisation=self.organisation,
            privacy=[self.organisation],
        )
        ResourceCategoryFeaturedFactory.create(
            category=self.resource_category,
            resource=resource,
        )
        response = self.app.get(
            reverse(
                'resources:resource-category-detail', kwargs={'slug': self.resource_category.slug}
            ),
            user=user,
        )
        featured_resources = response.context['featured_resources']
        self.assertTrue(featured_resources.exists())


class TestResourceCategoryListView(WebTest):

    def test_empty_return_code(self):
        response = self.app.get(reverse('resource-category-list'))
        self.assertEqual(response.status_code, 200)

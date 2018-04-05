from django.urls import reverse

from django_webtest import WebTest

from accounts.tests.factories import UserFactory
from comments.models import Comment, Report
from resources.tests.factories import ResourceFactory

from .factories import CommentFactory


class AddCommentTestView(WebTest):

    def setUp(self):
        self.resource = ResourceFactory.create(is_approved=True)
        self.superuser = UserFactory.create(password='test123')

    def test_post_comment_no_auth(self):
        response = self.app.get(self.resource.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertFalse('form' in response)

    def test_check_if_form_exists(self):
        response = self.app.get(self.resource.get_absolute_url(), user=self.superuser)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('form' in response)

    def test_post_method(self):
        form = self.app.get(self.resource.get_absolute_url(), user=self.superuser).form
        form['body'] = 'testing'
        response = form.submit()
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Comment.objects.filter(created_by=self.superuser).exists())


class ReportCommentView(WebTest):

    def setUp(self):
        self.comment = CommentFactory.create()
        self.superuser = UserFactory.create(password='test123')

    def test_post_method(self):
        form = self.app.get(
            reverse(
                'resources:resource-report-comment',
                kwargs={'slug': self.comment.resource.slug, 'id': self.comment.id}
            ),
            user=self.superuser,
        ).form

        form['body'] = 'testing'
        response = form.submit()
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Report.objects.filter(created_by=self.superuser).exists())


class UpdateCommentViewTEst(WebTest):

    def setUp(self):
        self.superuser = UserFactory.create(password='test123')
        self.comment = CommentFactory.create(body='test', created_by=self.superuser)

    def test_post_method(self):
        form = self.app.get(
            reverse(
                'resources:resource-update-comment',
                kwargs={'slug': self.comment.resource.slug, 'id': self.comment.id}
            ),
            user=self.superuser,
        ).form

        form['body'] = 'test123'
        response = form.submit()
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Comment.objects.filter(body='test123').exists())

import json

from rest_framework.test import APITestCase

from django.contrib.auth.models import User
from ..models import FriendStatus
from .. import tasks


class FriendshipTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create(username='john')
        self.user_2 = User.objects.create(username='two')

    def test_no_friends(self):
        resp = self.client.get('/user/{}/friendship'.format(self.user.pk))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data['results'], [])

    def test_become_friend_of_myself(self):
        resp = self.client.post('/user/{}/friendship'.format(self.user.pk),
                                json.dumps({'user': self.user.pk, 'target': self.user.pk}),
                                content_type='application/json')
        self.assertEqual(resp.status_code, 201, resp.content)

    def test_post_my_status(self):
        # make some friends
        resp = self.client.post('/user/{}/friendship'.format(self.user.pk),
                                json.dumps({'user': self.user_2.pk, 'target': self.user.pk}),
                                content_type='application/json')
        self.assertEqual(resp.status_code, 201, resp.content)
        # post status
        resp = self.client.post('/user/{}/status/me'.format(self.user.pk),
                                json.dumps({'content': 'hey', 'user': self.user.pk}),
                                content_type='application/json')
        self.assertEqual(resp.status_code, 201, resp.content)
        self.assertEqual(1, FriendStatus.objects.filter(user=self.user_2).count())

    def test_see_friends_posts(self):
        resp = self.client.get('/user/{}/status/all'.format(self.user.pk))
        self.assertEqual(resp.status_code, 200, resp.content)
        self.assertEqual(resp.data['results'], [])

    def test_dead_link_not_found(self):
        self.assertFalse(tasks._check_dead_links('ciao https://example.com ciao'))

    def test_dead_link_found(self):
        self.assertTrue(tasks._check_dead_links('ciao https://exampleeeeeeeeeeeeeeeeee.com ciao'))

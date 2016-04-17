import json

from rest_framework.test import APITestCase

from django.contrib.auth.models import User


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

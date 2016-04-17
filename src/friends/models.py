from django.db import models
from django.contrib.auth.models import User


class Friendship(models.Model):
    user = models.ForeignKey(User, related_name='outgoing_friendship_set')
    target = models.ForeignKey(User, related_name='incoming_friendship_set')

    def __str__(self):
        return 'Friendship {} user {} to user {}'.format(self.pk, self.user, self.target)


class Status(models.Model):
    user = models.ForeignKey(User)
    when = models.DateTimeField(auto_now_add=True)
    content = models.TextField(max_length=1024)
    followers_delivered = models.BooleanField(default=False)

    def __str__(self):
        return 'Status {} of user {} at {}'.format(self.pk, self.user, self.when and self.when.isoformat())


class FriendStatus(models.Model):
    user = models.ForeignKey(User)
    status = models.ForeignKey(Status)
    author = models.ForeignKey(User, related_name='outgoing_friendstatus_set')

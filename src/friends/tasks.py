from celery import task
from django.db import transaction

from .models import Status, FriendStatus


@task
def update_followers_status(status_id):
    """Locks status"""
    with transaction.atomic():
        status = Status.objects.select_for_update().get(pk=status_id)
        if status.followers_delivered:
            return
        for friendship in status.user.incoming_friendship_set.iterator():
            FriendStatus.objects.create(user=friendship.user, status=status, author=status.user)
        status.followers_delivered = True
        status.save(update_fields=['followers_delivered'])


import re

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


@task
def check_dead_links(status_id):
    status = Status.objects.get(pk=status_id)
    dead_links = _check_dead_links(status.content)
    if dead_links:
        print('dead links found in status {}'.format(status.pk))
    else:
        print('dead links NOT FOUND in status {}'.format(status.pk))


def _check_dead_links(text):
    import asyncio, aiohttp
    loop = asyncio.get_event_loop()
    links = re.findall(r'(https?://[^\s\']+/?)', text)
    tasks = []
    with aiohttp.ClientSession() as session:
        for link in links:
            tasks.append(asyncio.async(session.get(link)))
        done, pending = loop.run_until_complete(asyncio.wait(tasks, timeout=30))
    assert not pending
    for task in done:
        if task.exception():
            print('exception', task.exception())
            return True
    return False


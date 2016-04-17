from rest_framework.generics import ListAPIView, ListCreateAPIView
from rest_framework import permissions
from django.db import transaction

from . import models
from . import serializers
from . import filters
from . import tasks


class FriendshipList(ListCreateAPIView):
    queryset = models.Friendship.objects.all()
    serializer_class = serializers.FriendshipSerializer
    filter_backends = [filters.ByThisUserFilter]


class PersonalStatusList(ListCreateAPIView):
    queryset = models.Status.objects.all()
    serializer_class = serializers.StatusSerializer
    filter_backends = [filters.ByThisUserFilter]
    #permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        with transaction.atomic():
            status = serializer.save()
        tasks.update_followers_status.delay(status.pk)
        tasks.check_dead_links.delay(status.pk)
        return status

class AllStatusList(ListAPIView):
    queryset = models.Status.objects.all()
    serializer_class = serializers.StatusSerializer
    filter_backends = [filters.ByFriendsOfThisUserFilter]

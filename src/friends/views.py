from rest_framework.generics import ListAPIView, ListCreateAPIView
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

    def perform_create(self, serializer):
        with transaction.atomic():
            status = serializer.save()
        tasks.update_followers_status.delay(status.pk)
        return status

class AllStatusList(ListAPIView):
    queryset = models.Status.objects.all()
    serializer_class = serializers.StatusSerializer
    filter_backends = [filters.ByFriendsOfThisUserFilter]

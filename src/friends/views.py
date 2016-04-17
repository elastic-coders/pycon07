from rest_framework.generics import ListAPIView, ListCreateAPIView

from . import models
from . import serializers
from . import filters


class FriendshipList(ListCreateAPIView):
    queryset = models.Friendship.objects.all()
    serializer_class = serializers.FriendshipSerializer
    filter_backends = [filters.ByThisUserFilter]


class PersonalStatusList(ListCreateAPIView):
    queryset = models.Status.objects.all()
    serializer_class = serializers.StatusSerializer
    filter_backends = [filters.ByThisUserFilter]


class AllStatusList(ListAPIView):
    queryset = models.Status.objects.all()
    serializer_class = serializers.StatusSerializer
    filter_backends = [filters.ByFriendsOfThisUserFilter]

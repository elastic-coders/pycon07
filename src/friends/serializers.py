from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Friendship


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username']
        read_only_fields = ['id']


class FriendshipSerializer(serializers.ModelSerializer):

    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    target = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        fields = ['id', 'user', 'target']
        read_only_fields = ['id']
        model = Friendship


class StatusSerializer(serializers.ModelSerializer):

    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        fields = ['id', 'user', 'when', 'text']
        read_only_fields = ['id', 'when']
        model = Friendship

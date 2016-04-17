from rest_framework import filters

from . import models


class ByThisUserFilter(filters.BaseFilterBackend):

    def filter_queryset(self, request, queryset, view):
        return queryset.filter(user__id=view.kwargs['user_id'])


class ByFriendsOfThisUserFilter(filters.BaseFilterBackend):

    def filter_queryset(self, request, queryset, view):
        return queryset.filter(
            user__in=models.Friendship.values_list('target').filter(user__id=view.kwargs['user_id'])
        )

from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^user/(?P<user_id>\d+)/friendship$', views.FriendshipList.as_view()),
    url(r'^user/(?P<user_id>\d+)/status/me$', views.PersonalStatusList.as_view()),
    url(r'^user/(?P<user_id>\d+)/status/all$', views.AllStatusList.as_view()),
]

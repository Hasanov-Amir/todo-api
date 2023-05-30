from django.urls import path, include
from rest_framework import routers

from .views import GroupView, GroupMemberView


router = routers.SimpleRouter()
router.register(r'groups', GroupView)
router.register(r'groups-member', GroupMemberView)

urlpatterns = [
    path('', include(router.urls)),
]

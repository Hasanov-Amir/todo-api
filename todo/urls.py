from django.urls import path, include
from rest_framework import routers

from .views import TodoView


router = routers.SimpleRouter()
router.register(r'todos', TodoView)

urlpatterns = [
    path('', include(router.urls)),
]

from django.contrib import admin
from django.urls import re_path, path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('group.urls')),
    path('api/', include('todo.urls')),
    path('api/auth/', include('djoser.urls')),
    re_path(r'^api/auth/', include('djoser.urls.authtoken')),
]

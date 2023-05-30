from rest_framework import mixins, permissions, status
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from .models import Todo
from .permissions import TodoGetPermission, TodoGroupPermission
from .serializers import TodoSerializer


class TodoView(mixins.CreateModelMixin,
               mixins.UpdateModelMixin,
               mixins.ListModelMixin,
               mixins.RetrieveModelMixin,
               mixins.DestroyModelMixin,
               GenericViewSet):

    queryset = Todo.objects.all()
    serializer_class = TodoSerializer

    permission_classes = [
        permissions.IsAuthenticated,
        TodoGroupPermission,
        TodoGetPermission
    ]

    def create(self, request, *args, **kwargs):
        data = request.data
        data["todo_owner_id"] = request.user.id
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)



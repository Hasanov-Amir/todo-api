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

    def list(self, request, *args, **kwargs):
        group_id = self.request.query_params.get('group_id', False)
        if group_id:
            group_id = int(group_id)
            queryset = self.filter_queryset(
                self.get_queryset()
            ).filter(todo_group_id=group_id)

            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)

            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)

        error = {"error": "Please provide group_id in get parameters"}
        return Response(error, status=status.HTTP_400_BAD_REQUEST)

    def create(self, request, *args, **kwargs):
        data = request.data
        user = request.user
        data["todo_owner_id"] = user.id
        data["todo_owner_name"] = user.username
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)



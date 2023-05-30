from django.core.exceptions import ObjectDoesNotExist
from rest_framework import mixins, permissions, status
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from .serializers import GroupSerializer, GroupMemberSerializer
from .models import Group, GroupMember
from .permissions import GroupPermission, GroupMemberPermission


class GroupView(mixins.CreateModelMixin,
                mixins.UpdateModelMixin,
                mixins.ListModelMixin,
                mixins.RetrieveModelMixin,
                mixins.DestroyModelMixin,
                GenericViewSet):

    queryset = Group.objects.all()
    serializer_class = GroupSerializer

    permission_classes = [
        permissions.IsAuthenticated,
        GroupPermission,
    ]

    def list(self, request, *args, **kwargs):
        user_id = request.user.id
        list_of_participating_groups = GroupMember.objects.filter(group_member_id=user_id).values_list("group_id", flat=True)
        queryset = self.filter_queryset(self.get_queryset()).filter(id__in=list_of_participating_groups)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        data = serializer.data

        for d_group in data:
            group = Group.objects.get(id=d_group.get('id'))
            d_group.update(
                {
                    "members_count": group.members_count(),
                    "todos_count": group.todos_count()
                }
            )

        return Response(data)


class GroupMemberView(mixins.CreateModelMixin,
                      mixins.UpdateModelMixin,
                      mixins.ListModelMixin,
                      mixins.DestroyModelMixin,
                      GenericViewSet):

    queryset = GroupMember.objects.all()
    serializer_class = GroupMemberSerializer
    lookup_field = 'group_id'

    permission_classes = [
        permissions.IsAuthenticated,
        GroupMemberPermission,
    ]

    def create(self, request, *args, **kwargs):
        data = request.data

        if not (
                data.get("group_title", False) and
                data.get("group_password", False)
        ):
            error = {
                "group_title": [
                    "This field is required."
                ],
                "group_password": [
                    "This field is required."
                ]
            }
            return Response(error, status=status.HTTP_401_UNAUTHORIZED)

        data["group_member_id"] = request.user.id
        try:
            group = Group.objects.get(group_title=data['group_title'])
        except ObjectDoesNotExist:
            error = {"error": f"There is no group with this title: {data['group_title']}"}
            return Response(error, status=status.HTTP_400_BAD_REQUEST)

        data["group_id"] = group.id

        if not group.check_password(data["group_password"]):
            error = {"error": f"Invalid password"}
            return Response(error, status=status.HTTP_400_BAD_REQUEST)

        del data["group_title"]
        del data["group_password"]

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def destroy(self, request, *args, **kwargs):
        group_id = self.kwargs[self.lookup_field]
        user_id = request.user.id

        try:
            group = Group.objects.get(id=group_id)
        except ObjectDoesNotExist:
            error = {"error": f"Group with group_id={group_id} does not exists"}
            return Response(error, status=status.HTTP_400_BAD_REQUEST)

        group_owner_id = group.group_owner_id

        instance = GroupMember.objects.get(group_id=group_id, group_member_id=user_id)

        if user_id == group_owner_id:
            if group.members_count() == 1:
                group.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                random_member = GroupMember.objects.order_by('?')[0]
                group.group_owner_id = random_member.group_member_id
                group.save()
                random_member.delete()

        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def update(self, request, *args, **kwargs):
        group_id = self.kwargs[self.lookup_field]
        user_id = request.user.id

        try:
            group = Group.objects.get(id=group_id)
        except ObjectDoesNotExist:
            error = {"error": f"Group with group_id={group_id} does not exists"}
            return Response(error, status=status.HTTP_400_BAD_REQUEST)

        instance = GroupMember.objects.get(group_id=group_id, group_member_id=user_id)

        partial = kwargs.pop('partial', False)
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

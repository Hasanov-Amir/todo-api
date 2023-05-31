from rest_framework import permissions

from group.models import GroupMember, Group


class TodoGetPermission(permissions.BasePermission):
    message = "It is not your Todo"
    methods = ("GET", )

    def has_object_permission(self, request, view, obj):
        if request.method in self.methods:
            return True
        return obj.todo_owner_id == request.user.id


class TodoGroupPermission(permissions.BasePermission):
    message = "You are not listed in this group"
    methods = ("POST", "DELETE", "GET", "PUT")

    def has_object_permission(self, request, view, obj):
        if request.method in self.methods:
            user_id = request.user.id
            group_owner_id = Group.objects.get(id=obj.todo_group_id).id
            group_members_id_list = GroupMember.objects.filter(
                group_id=obj.todo_group_id
            ).values_list("group_member_id", flat=True)
            is_group_member = user_id in group_members_id_list
            is_group_owner = user_id == group_owner_id
            return is_group_member and is_group_owner
        return True

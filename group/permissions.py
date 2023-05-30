from rest_framework import permissions

from .models import GroupMember


class GroupPermission(permissions.BasePermission):
    message = "It is not your Group"
    methods = ("GET",)

    def has_object_permission(self, request, view, obj):
        if request.method in self.methods:
            return True
        return obj.group_owner_id == request.user.id  # or \
        # (request.user.id in GroupMember.objects.get(group_id=obj.id).values_list("group_member_id", flat=True))


class GroupMemberPermission(permissions.BasePermission):
    message = "You are not group admin"
    methods = ("DELETE", "PUT")

    def has_object_permission(self, request, view, obj):
        if request.method in self.methods:
            return obj.group_owner_id == request.user.id
        return True

from rest_framework import permissions


class TodoGetPermission(permissions.BasePermission):
    message = "It is not your Todo"
    methods = ("GET", )

    def has_object_permission(self, request, view, obj):
        if request.method in self.methods:
            return True
        return obj.group_owner_id == request.user.id


class TodoGroupPermission(permissions.BasePermission):
    message = "You are not listed in this group"
    methods = ("POST", "DELETE", "GET", "PUT")

    def has_object_permission(self, request, view, obj):
        if request.method in self.methods:
            return obj.group_owner_id == request.user.id
        return True

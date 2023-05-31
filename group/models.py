from django.db import models
from django.contrib.auth.models import User

from todo.models import Todo
from .utils import create_hash


class Group(models.Model):
    group_title = models.CharField(max_length=100, unique=True, verbose_name="Group Title")
    group_password = models.CharField(max_length=100, verbose_name="Group Password")
    group_description = models.TextField(verbose_name="Group Description")
    group_owner_id = models.PositiveSmallIntegerField(verbose_name="Group Owner ID")
    group_owner_name = models.CharField(max_length=100, verbose_name="Group Owner Name")
    group_create_datetime = models.DateTimeField(auto_now_add=True, verbose_name="Group Create Date and Time")
    group_edit_datetime = models.DateTimeField(auto_now=True, verbose_name="Group Edit Date and Time")

    def save(self, *args, **kwargs):
        self.group_password = create_hash(self.group_password)
        super().save(*args, **kwargs)

    def members_count(self):
        count = GroupMember.objects.filter(group_id=self.id).count()
        return count

    def todos_count(self):
        count = Todo.objects.filter(todo_group_id=self.id).count()
        return count

    def check_password(self, raw_password):
        hash_password = create_hash(raw_password)
        if self.group_password == hash_password:
            return True
        return False

    def __str__(self):
        return f"Title: {self.group_title}, Group Owner: {self.group_owner_id}"


class GroupMember(models.Model):
    group_member_id = models.PositiveSmallIntegerField(verbose_name="Group Member ID")
    group_member_is_admin = models.BooleanField(default=False, verbose_name="Group Member is Admin")
    group_id = models.PositiveSmallIntegerField(verbose_name="Group ID")
    member_join_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"User ID: {self.group_member_id}, Group ID: {self.group_id}, Is Admin: {self.group_member_is_admin}"

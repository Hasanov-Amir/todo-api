from django.db import models


class Todo(models.Model):
    todo_title = models.CharField(max_length=150, verbose_name="Todo Title")
    todo_is_complete = models.BooleanField(default=False, verbose_name="Todo is Complete")
    todo_create_datetime = models.DateTimeField(auto_now_add=True, verbose_name="Todo Create Date and Time")
    todo_edit_datetime = models.DateTimeField(auto_now=True, verbose_name="Todo Edit Date and Time")
    todo_owner_id = models.PositiveSmallIntegerField(verbose_name="Todo Owner ID")
    todo_owner_name = models.CharField(max_length=100, verbose_name="Todo Owner Name")
    todo_group_id = models.PositiveSmallIntegerField(verbose_name="Todo Group ID")

    def __str__(self):
        return f"Title: {self.todo_title}, Owner ID: {self.todo_owner_id}, Group ID: {self.todo_group_id}"

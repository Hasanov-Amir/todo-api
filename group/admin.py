from django.contrib import admin

from group.models import Group


class GroupAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'group_title',
        'group_owner_id',
        'group_create_datetime',
        'group_edit_datetime'
    )
    list_display_links = ('id', 'group_title')
    search_fields = ('id', 'group_title')


admin.site.register(Group, GroupAdmin)

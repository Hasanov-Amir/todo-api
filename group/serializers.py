import traceback

from rest_framework import serializers
from rest_framework.serializers import raise_errors_on_nested_writes

from group.models import Group, GroupMember


class GroupSerializer(serializers.ModelSerializer):
    members_count = serializers.ReadOnlyField(source='group.members_count')

    class Meta:
        model = Group
        extra_kwargs = {'group_password': {'write_only': True}}
        fields = '__all__'


class GroupMemberSerializer(serializers.ModelSerializer):

    class Meta:
        model = GroupMember
        fields = '__all__'

    def create(self, validated_data):

        raise_errors_on_nested_writes('create', self, validated_data)

        ModelClass = self.Meta.model

        try:
            instance = ModelClass._default_manager.create(**validated_data)
        except TypeError:
            tb = traceback.format_exc()
            msg = (
                'Got a `TypeError` when calling `%s.%s.create()`. '
                'This may be because you have a writable field on the '
                'serializer class that is not a valid argument to '
                '`%s.%s.create()`. You may need to make the field '
                'read-only, or override the %s.create() method to handle '
                'this correctly.\nOriginal exception was:\n %s' %
                (
                    ModelClass.__name__,
                    ModelClass._default_manager.name,
                    ModelClass.__name__,
                    ModelClass._default_manager.name,
                    self.__class__.__name__,
                    tb
                )
            )
            raise TypeError(msg)

        return instance

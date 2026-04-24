
from rest_framework import serializers
from .models import Community, CommunityMembership


class CommunityMembershipSerializer(serializers.ModelSerializer):
    """Сериализатор для участия в сообществе"""
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = CommunityMembership
        fields = ['id', 'user', 'username', 'role', 'joined_at']
        read_only_fields = ['user', 'joined_at']


class CommunitySerializer(serializers.ModelSerializer):
    """Сериализатор для сообществ"""
    creator_name = serializers.CharField(source='creator.username', read_only=True)
    members_count = serializers.SerializerMethodField()

    class Meta:
        model = Community
        fields = [
            'id', 'name', 'description', 'image', 'creator',
            'creator_name', 'is_private', 'created_at', 'members_count'
        ]
        read_only_fields = ['creator', 'created_at']

    def get_members_count(self, obj):
        return obj.memberships.count()


class CommunityListSerializer(serializers.ModelSerializer):
    """Краткий сериализатор для списка сообществ"""
    creator_name = serializers.CharField(source='creator.username', read_only=True)
    members_count = serializers.SerializerMethodField()

    class Meta:
        model = Community
        fields = ['id', 'name', 'description', 'image', 'creator_name', 'members_count']

    def get_members_count(self, obj):
        return obj.memberships.count()
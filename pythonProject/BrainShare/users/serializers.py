from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    """Сериализатор для профиля пользователя"""
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)

    class Meta:
        model = Profile
        fields = ['id', 'username', 'email', 'avatar', 'bio']
        read_only_fields = ['user']


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для пользователя"""
    notes_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'notes_count']
        read_only_fields = ['id']

    def get_notes_count(self, obj):
        return obj.notes.count()


class UserListSerializer(serializers.ModelSerializer):
    """Краткий сериализатор для списка пользователей"""
    notes_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'notes_count']

    def get_notes_count(self, obj):
        return obj.notes.count()
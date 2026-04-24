# memes/serializers.py
from rest_framework import serializers
from .models import Meme


class MemeSerializer(serializers.ModelSerializer):
    """Сериализатор для мемов"""
    author_name = serializers.CharField(source='author.username', read_only=True)

    class Meta:
        model = Meme
        fields = [
            'id', 'title', 'image_url', 'author', 'author_name',
            'created_at', 'is_approved', 'likes_count', 'description'
        ]
        read_only_fields = ['author', 'created_at', 'is_approved', 'likes_count']


class MemeListSerializer(serializers.ModelSerializer):
    """Краткий сериализатор для списка мемов"""
    author_name = serializers.CharField(source='author.username', read_only=True)

    class Meta:
        model = Meme
        fields = ['id', 'title', 'image_url', 'author_name', 'created_at', 'likes_count']
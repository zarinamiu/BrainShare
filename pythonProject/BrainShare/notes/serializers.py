from rest_framework import serializers
from .models import Note, Comment


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор для комментариев"""
    author_name = serializers.CharField(source='author.username', read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'author', 'author_name', 'text', 'created_at']
        read_only_fields = ['author', 'created_at']


class NoteSerializer(serializers.ModelSerializer):
    """Сериализатор для конспектов"""
    author_name = serializers.CharField(source='author.username', read_only=True)
    comments_count = serializers.SerializerMethodField()

    class Meta:
        model = Note
        fields = [
            'id', 'title', 'content', 'image', 'author', 'author_name',
            'created_at', 'updated_at', 'is_public', 'views_count',
            'subject', 'comments_count'
        ]
        read_only_fields = ['author', 'created_at', 'updated_at', 'views_count']

    def get_comments_count(self, obj):
        return obj.comments.count()


class NoteListSerializer(serializers.ModelSerializer):
    """Краткий сериализатор для списка конспектов"""
    author_name = serializers.CharField(source='author.username', read_only=True)
    comments_count = serializers.SerializerMethodField()

    class Meta:
        model = Note
        fields = [
            'id', 'title', 'author_name', 'created_at',
            'subject', 'views_count', 'comments_count', 'image'
        ]

    def get_comments_count(self, obj):
        return obj.comments.count()
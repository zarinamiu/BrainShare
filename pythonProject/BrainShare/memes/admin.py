from django.contrib import admin
from .models import Meme, UserProfile, Comment


@admin.register(Meme)
class MemeAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'likes_count', 'is_approved', 'created_at')
    list_editable = ('is_approved',)
    list_filter = ('is_approved', 'category', 'created_at')
    search_fields = ('title', 'description', 'author__username', 'category')
    ordering = ('-created_at',)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'university', 'course', 'favorite_memes_count')
    list_filter = ('university', 'course')
    search_fields = ('user__username', 'university', 'bio')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('meme', 'author', 'text_preview', 'created_at')
    list_filter = ('created_at', 'meme')
    search_fields = ('text', 'author__username')

    def text_preview(self, obj):
        return obj.text[:50] + '...' if len(obj.text) > 50 else obj.text

    text_preview.short_description = 'Текст'
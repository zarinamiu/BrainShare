from django.contrib import admin
from .models import Note, Comment


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'created_at', 'is_public', 'views_count']
    list_filter = ['is_public', 'subject', 'created_at']
    list_editable = ['is_public']
    search_fields = ['title', 'content', 'subject']
    readonly_fields = ['created_at', 'updated_at', 'views_count']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['note', 'author', 'text', 'created_at']
    list_filter = ['created_at']
    search_fields = ['text']
    readonly_fields = ['created_at']
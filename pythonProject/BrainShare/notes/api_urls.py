from django.urls import path
from .api_views import (
    NoteListAPIView, NoteDetailAPIView, NoteCreateAPIView,
    CommentListAPIView, CommentCreateAPIView
)

app_name = 'notes_api'

urlpatterns = [
    path('notes/', NoteListAPIView.as_view(), name='note-list'),
    path('notes/<int:note_id>/', NoteDetailAPIView.as_view(), name='note-detail'),
    path('notes/create/', NoteCreateAPIView.as_view(), name='note-create'),
    path('notes/<int:note_id>/comments/', CommentListAPIView.as_view(), name='comment-list'),
    path('notes/<int:note_id>/comments/create/', CommentCreateAPIView.as_view(), name='comment-create'),
]
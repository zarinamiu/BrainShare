from rest_framework import generics, permissions
from drf_spectacular.utils import extend_schema, OpenApiParameter
from .models import Note, Comment
from .serializers import NoteSerializer, NoteListSerializer, CommentSerializer


@extend_schema(
    tags=['Конспекты'],
    description='Список всех публичных конспектов'
)
class NoteListAPIView(generics.ListAPIView):
    """API для получения списка конспектов"""
    serializer_class = NoteListSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = Note.objects.filter(is_public=True)
        subject = self.request.query_params.get('subject')
        if subject:
            queryset = queryset.filter(subject__icontains=subject)
        return queryset


@extend_schema(
    tags=['Конспекты'],
    description='Детальная информация о конспекте'
)
class NoteDetailAPIView(generics.RetrieveAPIView):
    """API для получения деталей конспекта"""
    queryset = Note.objects.filter(is_public=True)
    serializer_class = NoteSerializer
    lookup_url_kwarg = 'note_id'


@extend_schema(
    tags=['Конспекты'],
    description='Создание нового конспекта'
)
class NoteCreateAPIView(generics.CreateAPIView):
    """API для создания конспекта"""
    serializer_class = NoteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


@extend_schema(
    tags=['Комментарии'],
    description='Список комментариев к конспекту',
    parameters=[
        OpenApiParameter(
            name='note_id',
            type=int,
            description='ID конспекта',
            required=True
        )
    ]
)
class CommentListAPIView(generics.ListAPIView):
    """API для получения комментариев к конспекту"""
    serializer_class = CommentSerializer

    def get_queryset(self):
        note_id = self.kwargs.get('note_id')
        return Comment.objects.filter(note_id=note_id)


@extend_schema(
    tags=['Комментарии'],
    description='Создание комментария'
)
class CommentCreateAPIView(generics.CreateAPIView):
    """API для создания комментария"""
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        note_id = self.kwargs.get('note_id')
        note = Note.objects.get(pk=note_id)
        serializer.save(author=self.request.user, note=note)
from rest_framework import generics, permissions
from drf_spectacular.utils import extend_schema
from .models import Meme
from .serializers import MemeSerializer, MemeListSerializer


@extend_schema(
    tags=['Мемы'],
    description='Список всех одобренных мемов'
)
class MemeListAPIView(generics.ListAPIView):
    """API для получения списка мемов"""
    serializer_class = MemeListSerializer

    def get_queryset(self):
        return Meme.objects.filter(is_approved=True)


@extend_schema(
    tags=['Мемы'],
    description='Детальная информация о меме'
)
class MemeDetailAPIView(generics.RetrieveAPIView):
    """API для получения деталей мема"""
    queryset = Meme.objects.filter(is_approved=True)
    serializer_class = MemeSerializer
    lookup_url_kwarg = 'meme_id'


@extend_schema(
    tags=['Мемы'],
    description='Создание нового мема'
)
class MemeCreateAPIView(generics.CreateAPIView):
    """API для создания мема"""
    serializer_class = MemeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
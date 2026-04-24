
from rest_framework import generics, permissions
from drf_spectacular.utils import extend_schema
from .models import Community
from .serializers import CommunitySerializer, CommunityListSerializer


@extend_schema(
    tags=['Сообщества'],
    description='Список всех сообществ'
)
class CommunityListAPIView(generics.ListAPIView):
    """API для получения списка сообществ"""
    serializer_class = CommunityListSerializer

    def get_queryset(self):
        queryset = Community.objects.all()
        is_private = self.request.query_params.get('is_private')
        if is_private is not None:
            queryset = queryset.filter(is_private=is_private.lower() == 'true')
        return queryset


@extend_schema(
    tags=['Сообщества'],
    description='Детальная информация о сообществе'
)
class CommunityDetailAPIView(generics.RetrieveAPIView):
    """API для получения деталей сообщества"""
    queryset = Community.objects.all()
    serializer_class = CommunitySerializer
    lookup_url_kwarg = 'community_id'


@extend_schema(
    tags=['Сообщества'],
    description='Создание нового сообщества'
)
class CommunityCreateAPIView(generics.CreateAPIView):
    """API для создания сообщества"""
    serializer_class = CommunitySerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)
from django.contrib.auth.models import User
from drf_spectacular.utils import extend_schema
from rest_framework import generics, permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Profile
from .serializers import ProfileSerializer, UserListSerializer, UserSerializer


@extend_schema(
    tags=['Пользователи'],
    description='Список пользователей'
)
class UserListAPIView(generics.ListAPIView):
    """API для получения списка пользователей"""
    queryset = User.objects.all()
    serializer_class = UserListSerializer


@extend_schema(
    tags=['Пользователи'],
    description='Информация о пользователе'
)
class UserDetailAPIView(generics.RetrieveAPIView):
    """API для получения информации о пользователе"""
    queryset = User.objects.all()
    serializer_class = UserSerializer


@extend_schema(
    tags=['Профили'],
    description='Профиль текущего пользователя'
)
class ProfileAPIView(generics.RetrieveUpdateAPIView):
    """API для профиля пользователя"""
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return Profile.objects.get(user=self.request.user)


@extend_schema(
    tags=['Пользователи'],
    description='Информация о текущем авторизованном пользователе'
)
class CurrentUserAPIView(APIView):
    """API для получения данных текущего пользователя"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        profile = getattr(user, 'profile', None)

        return Response({
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'bio': profile.bio if profile else '',
            'avatar': profile.avatar.url if profile and profile.avatar else None,
        })

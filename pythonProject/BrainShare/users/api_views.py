from rest_framework import generics, permissions
from drf_spectacular.utils import extend_schema
from django.contrib.auth.models import User
from .models import Profile
from .serializers import UserSerializer, UserListSerializer, ProfileSerializer


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
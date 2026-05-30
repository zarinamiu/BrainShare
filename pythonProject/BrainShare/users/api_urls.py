from django.urls import path
from .api_views import (
    UserListAPIView,
    UserDetailAPIView,
    ProfileAPIView,
    CurrentUserAPIView
)

app_name = 'users_api'

urlpatterns = [
    path('users/', UserListAPIView.as_view(), name='user-list'),
    path('users/<int:pk>/', UserDetailAPIView.as_view(), name='user-detail'),  # ← измени user_id на pk
    path('profile/', ProfileAPIView.as_view(), name='profile'),
    path('users/me/', CurrentUserAPIView.as_view(), name='api_current_user'),
]
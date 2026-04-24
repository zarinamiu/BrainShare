from django.urls import path
from .api_views import UserListAPIView, UserDetailAPIView, ProfileAPIView

app_name = 'users_api'

urlpatterns = [
    path('users/', UserListAPIView.as_view(), name='user-list'),
    path('users/<int:user_id>/', UserDetailAPIView.as_view(), name='user-detail'),
    path('profile/', ProfileAPIView.as_view(), name='profile'),
]
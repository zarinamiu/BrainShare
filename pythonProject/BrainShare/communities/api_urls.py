from django.urls import path
from .api_views import CommunityListAPIView, CommunityDetailAPIView, CommunityCreateAPIView

app_name = 'communities_api'

urlpatterns = [
    path('communities/', CommunityListAPIView.as_view(), name='community-list'),
    path('communities/<int:community_id>/', CommunityDetailAPIView.as_view(), name='community-detail'),
    path('communities/create/', CommunityCreateAPIView.as_view(), name='community-create'),
]
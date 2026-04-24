from django.urls import path
from .api_views import MemeListAPIView, MemeDetailAPIView, MemeCreateAPIView

app_name = 'memes_api'

urlpatterns = [
    path('memes/', MemeListAPIView.as_view(), name='meme-list'),
    path('memes/<int:meme_id>/', MemeDetailAPIView.as_view(), name='meme-detail'),
    path('memes/create/', MemeCreateAPIView.as_view(), name='meme-create'),
]
from django.urls import path
from . import views

app_name = 'memes'

urlpatterns = [
    path('', views.meme_list, name='meme_list'),
    path('create/', views.meme_create, name='meme_create'),
    path('meme/<int:meme_id>/', views.meme_detail, name='meme_detail'),
    path('meme/<int:meme_id>/edit/', views.meme_edit, name='meme_edit'),
    path('meme/<int:meme_id>/delete/', views.meme_delete, name='meme_delete'),
    path('comment/<int:comment_id>/edit/', views.comment_edit, name='comment_edit'),
    path('comment/<int:comment_id>/delete/', views.comment_delete, name='comment_delete'),
]

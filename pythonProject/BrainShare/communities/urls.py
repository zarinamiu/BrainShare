from django.urls import path
from . import views

app_name = 'communities'

urlpatterns = [
    path('', views.community_list, name='community_list'),
    path('create/', views.community_create, name='community_create'),
    path('<int:community_id>/', views.community_detail, name='community_detail'),
    path('<int:community_id>/join/', views.community_join, name='community_join'),
    path('<int:community_id>/leave/', views.community_leave, name='community_leave'),
]
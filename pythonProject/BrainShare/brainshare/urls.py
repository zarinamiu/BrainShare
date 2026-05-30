from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView
)

from . import views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', views.home, name='home'),
    path('toggle-banner/', views.toggle_banner, name='toggle_banner'),

    path('chat/', include('chat.urls', namespace='chat')),
    path('notes/', include('notes.urls', namespace='notes')),
    path('memes/', include('memes.urls', namespace='memes')),
    path('communities/', include('communities.urls', namespace='communities')),
    path('users/', include('users.urls', namespace='users')),

    path('accounts/', include('allauth.urls')),

    path('api/', include('notes.api_urls')),
    path('api/', include('communities.api_urls')),
    path('api/', include('memes.api_urls')),
    path('api/', include('users.api_urls')),

    path('api/auth/', include('dj_rest_auth.urls')),
    path('api/auth/registration/', include('dj_rest_auth.registration.urls')),

    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
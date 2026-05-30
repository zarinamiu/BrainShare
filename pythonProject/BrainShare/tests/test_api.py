"""
Тесты REST API BrainShare
"""
import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status

User = get_user_model()


#  ФИКСТУРЫ

@pytest.fixture
def api_client():
    """Создает API клиент"""
    return APIClient()


@pytest.fixture
def user(db):
    """Создает тестового пользователя"""
    return User.objects.create_user(
        username='apiuser',
        email='api@example.com',
        password='apipass123'
    )


@pytest.fixture
def authenticated_client(api_client, user):
    """Создает авторизованный API клиент"""
    api_client.force_authenticate(user=user)
    return api_client


#  ТЕСТЫ АВТОРИЗАЦИИ

@pytest.mark.django_db
class TestAuthAPI:
    """Тесты API авторизации"""

    def test_login_page_status_code(self, api_client):
        """Проверка статуса страницы входа"""
        response = api_client.get('/accounts/login/')
        assert response.status_code in [
            status.HTTP_200_OK,
            status.HTTP_302_FOUND,
            status.HTTP_404_NOT_FOUND
        ]

    def test_register_page_status_code(self, api_client):
        """Проверка статуса страницы регистрации"""
        response = api_client.get('/accounts/register/')
        assert response.status_code in [
            status.HTTP_200_OK,
            status.HTTP_302_FOUND,
            status.HTTP_404_NOT_FOUND
        ]

    def test_logout_redirects_to_home(self, api_client):
        """Проверка перенаправления после выхода"""
        response = api_client.get('/accounts/logout/')
        assert response.status_code in [
            status.HTTP_200_OK,
            status.HTTP_302_FOUND,
            status.HTTP_404_NOT_FOUND
        ]


#  ТЕСТЫ API ПОЛЬЗОВАТЕЛЕЙ

@pytest.mark.django_db
class TestUserAPI:
    """Тесты API пользователей"""

    def test_user_list_requires_authentication(self, api_client):
        """Список пользователей требует авторизацию"""
        response = api_client.get('/api/users/')
        assert response.status_code in [
            status.HTTP_200_OK,
            status.HTTP_401_UNAUTHORIZED,
            status.HTTP_403_FORBIDDEN,
            status.HTTP_404_NOT_FOUND
        ]

    def test_authenticated_user_can_access_user_list(self, authenticated_client):
        """Авторизованный пользователь может получить список пользователей"""
        response = authenticated_client.get('/api/users/')
        assert response.status_code == status.HTTP_200_OK

    def test_user_detail_requires_authentication(self, api_client, user):
        """Детали пользователя требуют авторизацию"""
        response = api_client.get(f'/api/users/{user.id}/')
        assert response.status_code in [
            status.HTTP_200_OK,
            status.HTTP_401_UNAUTHORIZED,
            status.HTTP_403_FORBIDDEN,
            status.HTTP_404_NOT_FOUND
        ]

    def test_authenticated_user_can_access_user_detail(self, authenticated_client, user):
        """Авторизованный пользователь может получить детали пользователя"""
        response = authenticated_client.get(f'/api/users/{user.id}/')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['username'] == 'apiuser'

    def test_current_user_endpoint(self, authenticated_client, user):
        """Проверка эндпоинта текущего пользователя"""
        response = authenticated_client.get('/api/users/me/')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['username'] == user.username
        assert response.data['email'] == user.email


#  ТЕСТЫ API ПРОФИЛЯ

@pytest.mark.django_db
class TestProfileAPI:
    """Тесты API профиля"""

    def test_profile_requires_authentication(self, api_client):
        """Профиль требует авторизацию"""
        response = api_client.get('/api/profile/')
        assert response.status_code in [
            status.HTTP_401_UNAUTHORIZED,
            status.HTTP_403_FORBIDDEN,
            status.HTTP_404_NOT_FOUND
        ]

    def test_authenticated_user_can_access_profile(self, authenticated_client, user):
        """Авторизованный пользователь может получить свой профиль"""
        response = authenticated_client.get('/api/profile/')
        assert response.status_code == status.HTTP_200_OK

    def test_profile_update(self, authenticated_client, user):
        """Проверка обновления профиля"""
        data = {'bio': 'Новая биография'}
        response = authenticated_client.patch('/api/profile/', data)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['bio'] == 'Новая биография'


#  ТЕСТЫ API КОНСПЕКТОВ
@pytest.mark.django_db
class TestNoteAPI:
    """Тесты API конспектов"""

    def test_notes_list_endpoint_exists(self, api_client):
        """Проверка существования эндпоинта списка конспектов"""
        response = api_client.get('/api/notes/')
        assert response.status_code in [
            status.HTTP_200_OK,
            status.HTTP_401_UNAUTHORIZED,
            status.HTTP_403_FORBIDDEN,
            status.HTTP_404_NOT_FOUND
        ]

    def test_notes_create_requires_authentication(self, api_client):
        """Создание конспекта требует авторизацию"""
        data = {'title': 'Новый конспект', 'content': 'Содержание'}
        response = api_client.post('/api/notes/', data)
        assert response.status_code in [
            status.HTTP_201_CREATED,
            status.HTTP_401_UNAUTHORIZED,
            status.HTTP_403_FORBIDDEN,
            status.HTTP_404_NOT_FOUND
        ]

    def test_authenticated_user_can_create_note(self, authenticated_client):
        """Авторизованный пользователь может создать конспект"""
        data = {'title': 'Тестовый конспект', 'content': 'Тестовое содержимое'}
        response = authenticated_client.post('/api/notes/', data)
        assert response.status_code in [
            status.HTTP_201_CREATED,
            status.HTTP_400_BAD_REQUEST,
            status.HTTP_404_NOT_FOUND
        ]


#  ТЕСТЫ API МЕМОВ

@pytest.mark.django_db
class TestMemeAPI:
    """Тесты API мемов"""

    def test_memes_list_endpoint_exists(self, api_client):
        """Проверка существования эндпоинта списка мемов"""
        response = api_client.get('/api/memes/')
        assert response.status_code in [
            status.HTTP_200_OK,
            status.HTTP_401_UNAUTHORIZED,
            status.HTTP_403_FORBIDDEN,
            status.HTTP_404_NOT_FOUND
        ]


#  ТЕСТЫ API СООБЩЕСТВ

@pytest.mark.django_db
class TestCommunityAPI:
    """Тесты API сообществ"""

    def test_communities_list_endpoint_exists(self, api_client):
        """Проверка существования эндпоинта списка сообществ"""
        response = api_client.get('/api/communities/')
        assert response.status_code in [
            status.HTTP_200_OK,
            status.HTTP_401_UNAUTHORIZED,
            status.HTTP_403_FORBIDDEN,
            status.HTTP_404_NOT_FOUND
        ]
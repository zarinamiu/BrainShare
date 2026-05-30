"""
Тесты моделей данных BrainShare
"""
import pytest
from django.contrib.auth import get_user_model

User = get_user_model()


# ФИКСТУРЫ

@pytest.fixture
def user(db):
    """Создает тестового пользователя"""
    return User.objects.create_user(
        username='testuser',
        email='test@example.com',
        password='testpass123'
    )


@pytest.fixture
def user2(db):
    """Создает второго тестового пользователя"""
    return User.objects.create_user(
        username='testuser2',
        email='test2@example.com',
        password='testpass123'
    )


@pytest.fixture
def superuser(db):
    """Создает суперпользователя"""
    return User.objects.create_superuser(
        username='admin',
        email='admin@example.com',
        password='adminpass123'
    )


# ТЕСТЫ МОДЕЛИ USER

@pytest.mark.django_db
class TestUser:
    """Тесты модели User"""

    def test_user_creation(self, user):
        """Проверка создания пользователя с корректными данными"""
        assert user.username == 'testuser'
        assert user.email == 'test@example.com'
        assert user.check_password('testpass123')
        assert user.is_active is True
        assert user.is_staff is False
        assert user.is_superuser is False

    def test_user_str(self, user):
        """Проверка строкового представления пользователя"""
        assert str(user) == 'testuser'

    def test_user_full_name(self, user):
        """Проверка метода get_full_name()"""
        user.first_name = 'Иван'
        user.last_name = 'Иванов'
        user.save()
        assert user.get_full_name() == 'Иван Иванов'

    def test_user_short_name(self, user):
        """Проверка метода get_short_name()"""
        user.first_name = 'Иван'
        user.save()
        assert user.get_short_name() == 'Иван'

    def test_user_username_unique(self, user):
        """Проверка уникальности username"""
        with pytest.raises(Exception):
            User.objects.create_user(
                username='testuser',
                email='another@example.com',
                password='pass123'
            )

    def test_user_password_hashing(self, user):
        """Проверка хеширования пароля"""
        assert user.password != 'testpass123'
        assert user.password.startswith('pbkdf2_sha256$')

    def test_user_password_verification(self, user):
        """Проверка верификации пароля"""
        assert user.check_password('testpass123') is True
        assert user.check_password('wrongpassword') is False


#  ТЕСТЫ МОДЕЛИ PROFILE

@pytest.mark.django_db
class TestProfile:
    """Тесты модели Profile"""

    def test_profile_creation_on_user_creation(self):
        """При создании пользователя должен создаваться профиль"""
        from users.models import Profile

        user = User.objects.create_user(
            username='newuser',
            email='newuser@example.com',
            password='pass123'
        )

        assert Profile.objects.filter(user=user).exists()

    def test_profile_str(self, user):
        """Проверка строкового представления профиля"""
        from users.models import Profile
        profile = Profile.objects.get(user=user)
        assert user.username in str(profile)

    def test_profile_bio(self, user):
        """Проверка поля bio профиля"""
        from users.models import Profile
        profile = Profile.objects.get(user=user)

        profile.bio = 'Это тестовая биография'
        profile.save()

        profile.refresh_from_db()
        assert profile.bio == 'Это тестовая биография'

    def test_profile_default_bio_empty(self, user):
        """Проверка пустого bio по умолчанию"""
        from users.models import Profile
        profile = Profile.objects.get(user=user)
        assert profile.bio == '' or profile.bio is None

    def test_user_email_update(self, user):
        """Проверка обновления email пользователя"""
        user.email = 'newemail@example.com'
        user.save()

        user.refresh_from_db()
        assert user.email == 'newemail@example.com'

    def test_user_password_change(self, user):
        """Проверка смены пароля через set_password()"""
        user.set_password('newpassword123')
        user.save()

        user.refresh_from_db()
        assert user.check_password('newpassword123') is True
        assert user.check_password('testpass123') is False

    def test_profile_one_to_one_relationship(self, user):
        """Проверка связи один-к-одному между User и Profile"""
        from users.models import Profile
        profile = Profile.objects.get(user=user)

        assert profile.user == user
        assert hasattr(user, 'profile')


# ТЕСТЫ СУПЕРПОЛЬЗОВАТЕЛЯ

@pytest.mark.django_db
class TestSuperuser:
    """Тесты суперпользователя"""

    def test_superuser_creation(self, superuser):
        """Проверка создания суперпользователя"""
        assert superuser.username == 'admin'
        assert superuser.email == 'admin@example.com'
        assert superuser.is_superuser is True
        assert superuser.is_staff is True

    def test_superuser_can_access_admin(self, superuser):
        """Проверка доступа суперпользователя к админке"""
        assert superuser.has_perm('can_access_admin') is True

    def test_superuser_permissions(self, superuser):
        """Проверка прав суперпользователя"""
        assert superuser.has_perm('any_permission') is True
        assert superuser.has_module_perms('any_app') is True


#  ТЕСТЫ КОЛИЧЕСТВА ПОЛЬЗОВАТЕЛЕЙ

@pytest.mark.django_db
class TestUserCounts:
    """Тесты подсчета пользователей"""

    def test_user_count_after_creation(self):
        """Проверка увеличения счетчика при создании пользователей"""
        initial_count = User.objects.count()

        User.objects.create_user(username='user1', email='user1@test.com', password='pass1')
        User.objects.create_user(username='user2', email='user2@test.com', password='pass2')
        User.objects.create_user(username='user3', email='user3@test.com', password='pass3')

        final_count = User.objects.count()
        assert final_count == initial_count + 3

    def test_user_count_after_deletion(self, user, user2):
        """Проверка уменьшения счетчика при удалении пользователей"""
        initial_count = User.objects.count()

        user.delete()

        final_count = User.objects.count()
        assert final_count == initial_count - 1
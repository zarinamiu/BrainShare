from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile

@receiver(post_save, sender=User)
def create_profile_for_new_user(sender, instance, created, **kwargs):
    """Создаёт профиль автоматически при создании нового пользователя"""
    if created:
        Profile.objects.get_or_create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Обновляет профиль при сохранении данных пользователя"""
    # Проверка hasattr нужна, чтобы код не упал, если профиля вдруг нет
    if hasattr(instance, 'profile'):
        instance.profile.save()

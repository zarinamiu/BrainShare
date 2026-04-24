from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile'
    )
    avatar = models.ImageField(
        upload_to='avatars/',
        default='avatars/default.png',
        verbose_name="Аватар",
        blank=True
    )
    bio = models.TextField(
        max_length=500,
        blank=True,
        verbose_name="О себе"
    )
    
    class Meta:
        verbose_name = "Профиль"
        verbose_name_plural = "Профили"
    
    def __str__(self):
        return f"Профиль {self.user.username}"

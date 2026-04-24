from django.db import models
from django.contrib.auth.models import User


class Community(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название")
    description = models.TextField(verbose_name="Описание", blank=True)
    image = models.ImageField(
        upload_to='communities/',
        verbose_name="Изображение",
        blank=True,
        null=True
    )
    creator = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='created_communities',
        verbose_name="Создатель"
    )
    members = models.ManyToManyField(
        User,
        through='CommunityMembership',
        related_name='communities',
        verbose_name="Участники"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    is_private = models.BooleanField(default=False, verbose_name="Приватное")
    
    class Meta:
        verbose_name = "Сообщество"
        verbose_name_plural = "Сообщества"
        ordering = ['-created_at']
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('communities:community_detail', kwargs={'community_id': self.pk})
    
    @property
    def members_count(self):
        return self.members.count()


class CommunityMembership(models.Model):
    ROLE_CHOICES = [
        ('member', 'Участник'),
        ('moderator', 'Модератор'),
        ('admin', 'Администратор'),
    ]
    
    community = models.ForeignKey(
        Community,
        on_delete=models.CASCADE,
        related_name='memberships'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='community_memberships'
    )
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='member',
        verbose_name="Роль"
    )
    joined_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата вступления")
    
    class Meta:
        verbose_name = "Членство в сообществе"
        verbose_name_plural = "Членства в сообществах"
        unique_together = ['community', 'user']
    
    def __str__(self):
        return f"{self.user.username} в {self.community.name} ({self.get_role_display()})"

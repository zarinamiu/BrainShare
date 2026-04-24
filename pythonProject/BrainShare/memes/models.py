from django.db import models
from django.contrib.auth.models import User


class Meme(models.Model):
    title = models.CharField(max_length=200, verbose_name="Заголовок")
    image_url = models.URLField(verbose_name="Ссылка на изображение")
    description = models.TextField(verbose_name="Описание", blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='memes', verbose_name="Автор")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    likes_count = models.IntegerField(default=0, verbose_name="Лайков")
    is_approved = models.BooleanField(default=True, verbose_name="Одобрено")
    category = models.CharField(max_length=50, verbose_name="Категория", default="Общее")

    class Meta:
        verbose_name = "Мем"
        verbose_name_plural = "Мемы"
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    bio = models.TextField(verbose_name="О себе", blank=True)
    university = models.CharField(max_length=100, verbose_name="Университет", blank=True)
    course = models.IntegerField(verbose_name="Курс", null=True, blank=True)
    favorite_memes_count = models.IntegerField(default=0, verbose_name="Избранных мемов")

    class Meta:
        verbose_name = "Профиль пользователя"
        verbose_name_plural = "Профили пользователей"

    def __str__(self):
        return f"Профиль {self.user.username}"


class Comment(models.Model):
    meme = models.ForeignKey(
        'Meme',
        verbose_name='Мем',
        on_delete=models.CASCADE,
        related_name='comments'
    )
    author = models.ForeignKey(
        User,
        verbose_name='Автор',
        on_delete=models.CASCADE,
        related_name='memes_comments'
    )
    text = models.TextField('Текст комментария')
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['-created_at']

    def __str__(self):
        return f'Комментарий от {self.author} к {self.meme.title}'
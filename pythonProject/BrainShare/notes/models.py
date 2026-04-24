from django.db import models
from django.contrib.auth.models import User


class Note(models.Model):
    title = models.CharField(max_length=200, verbose_name="Заголовок")
    content = models.TextField(verbose_name="Содержание")
    image = models.ImageField(
        upload_to='notes_images/',
        verbose_name="Изображение",
        blank=True,
        null=True
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='notes',
        verbose_name="Автор"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    is_public = models.BooleanField(default=True, verbose_name="Публичная")
    views_count = models.IntegerField(default=0, verbose_name="Просмотров")
    subject = models.CharField(max_length=100, verbose_name="Предмет", blank=True)

    class Meta:
        verbose_name = "Конспект"
        verbose_name_plural = "Конспекты"
        ordering = ['-created_at']

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('notes:note_detail', kwargs={'note_id': self.pk})


class Comment(models.Model):
    note = models.ForeignKey(
        'Note',
        verbose_name='Конспект',
        on_delete=models.CASCADE,
        related_name='comments'
    )
    author = models.ForeignKey(
        User,
        verbose_name='Автор',
        on_delete=models.CASCADE,
        related_name='notes_comments'
    )
    text = models.TextField('Текст комментария')
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['-created_at']

    def __str__(self):
        return f'Комментарий от {self.author} к {self.note.title}'

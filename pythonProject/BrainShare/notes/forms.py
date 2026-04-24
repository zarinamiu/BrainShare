from django import forms
from .models import Note, Comment


class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['title', 'content', 'image', 'subject', 'is_public']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Заголовок конспекта'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-textarea',
                'placeholder': 'Содержание конспекта...',
                'rows': 10
            }),
            'subject': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Например: Математика'
            }),
        }
        labels = {
            'title': 'Заголовок',
            'content': 'Содержание',
            'image': 'Изображение',
            'subject': 'Предмет',
            'is_public': 'Публичный конспект'
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={
                'class': 'form-textarea',
                'placeholder': 'Напишите комментарий...',
                'rows': 3
            })
        }
        labels = {
            'text': 'Комментарий'
        }

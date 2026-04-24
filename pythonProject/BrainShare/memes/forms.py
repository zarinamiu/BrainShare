from django import forms
from .models import Meme, Comment


class MemeForm(forms.ModelForm):
    class Meta:
        model = Meme
        fields = ['title', 'image_url', 'description', 'category']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Заголовок мема'
            }),
            'image_url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://example.com/meme.jpg'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Описание мема...'
            }),
            'category': forms.Select(attrs={
                'class': 'form-control'
            }),
        }
        labels = {
            'title': 'Заголовок',
            'image_url': 'Ссылка на изображение',
            'description': 'Описание',
            'category': 'Категория'
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Напишите ваш комментарий...',
                'style': 'width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 5px;'
            })
        }
        labels = {
            'text': 'Ваш комментарий'
        }

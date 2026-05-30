from django import forms
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, render

from .models import Profile


# ==========================================
# ФОРМЫ (Перенесено из второго куска)
# ==========================================
class RegisterForm(forms.ModelForm):
    password1 = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={'placeholder': 'Введите пароль'})
    )
    password2 = forms.CharField(
        label='Подтверждение пароля',
        widget=forms.PasswordInput(attrs={'placeholder': 'Повторите пароль'})
    )

    class Meta:
        model = User
        fields = ['username', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Введите имя пользователя'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Введите email'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Пароли не совпадают')

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


# ==========================================
# ПРЕДСТАВЛЕНИЯ (VIEWS)
# ==========================================

class CustomLoginView(LoginView):
    """Вход в аккаунт на основе стандартного класса Django"""
    template_name = 'users/login.html'
    authentication_form = AuthenticationForm


def register_view(request):
    """Регистрация пользователя с использованием RegisterForm"""
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Автоматически создаем профиль для нового пользователя
            Profile.objects.get_or_create(user=user)
            login(request, user)
            messages.success(request, 'Регистрация прошла успешно!')
            return redirect('home')
    else:
        form = RegisterForm()

    return render(request, 'users/register.html', {'form': form})


def logout_view(request):
    """Выход из аккаунта"""
    logout(request)
    messages.success(request, 'Вы вышли из аккаунта')
    return redirect('home')


@login_required
def profile_view(request):
    """Просмотр и редактирование профиля (Объединенная логика)"""
    user = request.user
    # Гарантируем, что объект профиля существует
    profile_obj, created = Profile.objects.get_or_create(user=user)

    # Обработка обновления аватара
    if request.POST.get('update_avatar') and request.FILES.get('avatar'):
        profile_obj.avatar = request.FILES['avatar']
        profile_obj.save()
        messages.success(request, 'Аватар обновлён!')
        return redirect('users:profile')

    # Обработка текстовых данных профиля
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        bio = request.POST.get('bio', '').strip()

        if username:
            # Проверяем, не занят ли username другим пользователем
            if User.objects.filter(username=username).exclude(pk=user.pk).exists():
                messages.error(request, 'Это имя пользователя уже занято')
                return redirect('users:profile')
            user.username = username

        user.email = email
        user.save()

        profile_obj.bio = bio
        profile_obj.save()

        messages.success(request, 'Профиль успешно обновлён!')
        return redirect('users:profile')

    # Передаем в контекст и профиль, и пользователя под обоими именами для совместимости с шаблонами
    context = {
        'profile': profile_obj,
        'user_obj': user
    }
    return render(request, 'users/profile.html', context)

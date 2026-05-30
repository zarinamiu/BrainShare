from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Profile

# 1. Настройка инлайна профиля для админки пользователя
class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Профиль'

# 2. Кастомизация админки пользователя
class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline,)

# Перерегистрация стандартной модели User
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

# 3. Регистрация и настройка отдельного управления профилями
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created_at')
    search_fields = ('user__username', 'user__email')
    list_filter = ('created_at',)

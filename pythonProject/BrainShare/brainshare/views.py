from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST

from communities.models import Community
from memes.models import Meme
from notes.models import Note


def home(request):
    """Главная страница со списками последних публикаций"""
    # Получаем состояние баннера из сессии (по умолчанию True)
    show_banner = request.session.get('show_banner', True)

    # Загружаем последние 5 записей для каждого раздела
    recent_notes = Note.objects.all()[:5]
    recent_memes = Meme.objects.all()[:5]
    recent_communities = Community.objects.all()[:5]  # Добавлено на будущее, так как модель импортирована

    context = {
        'show_banner': show_banner,
        'recent_notes': recent_notes,
        'recent_memes': recent_memes,
        'recent_communities': recent_communities,
    }
    return render(request, 'home.html', context)


@require_POST
def toggle_banner(request):
    """Переключение видимости баннера (поддерживает обычный POST и AJAX/Fetch)"""
    # Проверяем значение из POST-запроса
    show = request.POST.get('show', 'true') == 'true'
    request.session['show_banner'] = show

    # Если запрос пришел через JavaScript (Fetch/Axios/AJAX)
    if request.headers.get('x-requested-with') == 'XMLHttpRequest' or request.content_type == 'application/json':
        return JsonResponse({"status": "ok", "show_banner": show})

    # Если это обычная отправка HTML-формы, перенаправляем на главную
    return redirect('home')

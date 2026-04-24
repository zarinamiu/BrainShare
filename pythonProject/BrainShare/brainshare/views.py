from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from notes.models import Note
from memes.models import Meme
from communities.models import Community


def home(request):
    """Главная страница"""
    show_banner = request.session.get('show_banner', True)

    recent_notes = Note.objects.all()[:5]
    recent_memes = Meme.objects.all()[:5]

    return render(request, 'home.html', {
        'show_banner': show_banner,
        'recent_notes': recent_notes,
        'recent_memes': recent_memes,
    })


@require_POST
def toggle_banner(request):
    show = request.POST.get('show', 'true') == 'true'
    request.session['show_banner'] = show
    return redirect('home')
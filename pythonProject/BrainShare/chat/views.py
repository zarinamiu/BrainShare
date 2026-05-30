from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render, redirect

AVAILABLE_ROOMS = [
    'general',
    'support',
    'study',
    'python',
    'django',
]


@login_required
def room_list(request):
    return redirect('chat:room', room_name='general')


@login_required
def room(request, room_name):
    if room_name not in AVAILABLE_ROOMS:
        raise Http404('Такой комнаты не существует')

    return render(request, 'chat/room.html', {
        'room_name': room_name,
        'rooms': AVAILABLE_ROOMS,
    })

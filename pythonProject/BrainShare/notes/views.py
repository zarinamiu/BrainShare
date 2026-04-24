from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Note, Comment
from .forms import NoteForm, CommentForm


def note_list(request):
    """Список всех публичных конспектов"""
    notes = Note.objects.filter(is_public=True).order_by('-created_at')

    viewed_ids = request.session.get('viewed_notes', [])
    recently_viewed = Note.objects.filter(id__in=viewed_ids[:5]) if viewed_ids else []

    return render(request, 'notes/list.html', {
        'notes': notes,
        'recently_viewed': recently_viewed,
    })


def note_detail(request, note_id):
    """Детальная страница конспекта"""
    note = get_object_or_404(Note, id=note_id)
    comments = note.comments.all().order_by('-created_at')

    note.views_count += 1
    note.save(update_fields=['views_count'])

    viewed_ids = request.session.get('viewed_notes', [])

    if note_id in viewed_ids:
        viewed_ids.remove(note_id)
    viewed_ids.insert(0, note_id)

    request.session['viewed_notes'] = viewed_ids[:10]
    request.session.modified = True

    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('users:login')

        form = CommentForm(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.note = note
            new_comment.author = request.user
            new_comment.save()
            messages.success(request, 'Комментарий добавлен!')
            return redirect('notes:note_detail', note_id=note.id)
    else:
        form = CommentForm()

    context = {
        'note': note,
        'comments': comments,
        'form': form
    }
    return render(request, 'notes/detail.html', context)


def clear_viewed_history(request):
    """Очистка истории просмотров"""
    request.session['viewed_notes'] = []
    request.session.modified = True
    messages.success(request, 'История просмотров очищена!')
    return redirect('notes:note_list')


@login_required
def note_create(request):
    """Создание конспекта"""
    if request.method == 'POST':
        form = NoteForm(request.POST, request.FILES)
        if form.is_valid():
            note = form.save(commit=False)
            note.author = request.user
            note.save()
            messages.success(request, 'Конспект успешно создан!')
            return redirect('notes:note_detail', note_id=note.id)
    else:
        form = NoteForm()
    return render(request, 'notes/form.html', {'form': form, 'title': 'Создать конспект'})


@login_required
def note_edit(request, note_id):
    """Редактирование конспекта"""
    note = get_object_or_404(Note, id=note_id)

    if note.author != request.user:
        messages.error(request, 'У вас нет прав на редактирование этого конспекта!')
        return redirect('notes:note_detail', note_id=note.id)

    if request.method == 'POST':
        form = NoteForm(request.POST, request.FILES, instance=note)
        if form.is_valid():
            form.save()
            messages.success(request, 'Конспект обновлен!')
            return redirect('notes:note_detail', note_id=note.id)
    else:
        form = NoteForm(instance=note)

    return render(request, 'notes/form.html', {'form': form, 'title': 'Редактировать конспект', 'note': note})


@login_required
def note_delete(request, note_id):
    """Удаление конспекта"""
    note = get_object_or_404(Note, id=note_id)

    if note.author != request.user:
        messages.error(request, 'У вас нет прав на удаление этого конспекта!')
        return redirect('notes:note_detail', note_id=note.id)

    if request.method == 'POST':
        note.delete()
        messages.success(request, 'Конспект удален!')
        return redirect('notes:note_list')

    return render(request, 'notes/confirm_delete.html', {'note': note})


@login_required
def comment_edit(request, comment_id):
    """Редактирование комментария"""
    comment = get_object_or_404(Comment, id=comment_id)

    if comment.author != request.user:
        messages.error(request, 'У вас нет прав на редактирование этого комментария!')
        return redirect('notes:note_detail', note_id=comment.note.id)

    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            messages.success(request, 'Комментарий обновлен!')
            return redirect('notes:note_detail', note_id=comment.note.id)
    else:
        form = CommentForm(instance=comment)

    return render(request, 'notes/comment_form.html', {
        'form': form,
        'comment': comment,
        'note': comment.note
    })


@login_required
def comment_delete(request, comment_id):
    """Удаление комментария"""
    comment = get_object_or_404(Comment, id=comment_id)

    if comment.author != request.user:
        messages.error(request, 'У вас нет прав на удаление этого комментария!')
        return redirect('notes:note_detail', note_id=comment.note.id)

    note_id = comment.note.id

    if request.method == 'POST':
        comment.delete()
        messages.success(request, 'Комментарий удален!')
        return redirect('notes:note_detail', note_id=note_id)

    return render(request, 'notes/confirm_delete_comment.html', {'comment': comment})

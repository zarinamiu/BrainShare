from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Meme, Comment
from .forms import MemeForm, CommentForm


def meme_list(request):
    memes = Meme.objects.all().order_by('-created_at')
    return render(request, 'memes/list.html', {'memes': memes})


def meme_detail(request, meme_id):
    meme = get_object_or_404(Meme, id=meme_id)
    comments = meme.comments.all().order_by('-created_at')

    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('users:login')

        form = CommentForm(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.meme = meme
            new_comment.author = request.user
            new_comment.save()
            messages.success(request, 'Комментарий добавлен!')
            return redirect('memes:meme_detail', meme_id=meme.id)
    else:
        form = CommentForm()

    context = {
        'meme': meme,
        'comments': comments,
        'form': form
    }
    return render(request, 'memes/detail.html', context)


@login_required
def meme_create(request):
    if request.method == 'POST':
        form = MemeForm(request.POST)
        if form.is_valid():
            meme = form.save(commit=False)
            meme.author = request.user
            meme.save()
            messages.success(request, 'Мем успешно создан!')
            return redirect('memes:meme_detail', meme_id=meme.id)
    else:
        form = MemeForm()
    return render(request, 'memes/form.html', {'form': form, 'title': 'Создать мем'})


@login_required
def meme_edit(request, meme_id):
    meme = get_object_or_404(Meme, id=meme_id)
    
    if meme.author != request.user:
        messages.error(request, 'У вас нет прав на редактирование этого мема!')
        return redirect('memes:meme_detail', meme_id=meme.id)
    
    if request.method == 'POST':
        form = MemeForm(request.POST, instance=meme)
        if form.is_valid():
            form.save()
            messages.success(request, 'Мем обновлен!')
            return redirect('memes:meme_detail', meme_id=meme.id)
    else:
        form = MemeForm(instance=meme)
    
    return render(request, 'memes/form.html', {'form': form, 'title': 'Редактировать мем', 'meme': meme})


@login_required
def meme_delete(request, meme_id):
    meme = get_object_or_404(Meme, id=meme_id)
    
    if meme.author != request.user:
        messages.error(request, 'У вас нет прав на удаление этого мема!')
        return redirect('memes:meme_detail', meme_id=meme.id)
    
    if request.method == 'POST':
        meme.delete()
        messages.success(request, 'Мем удален!')
        return redirect('memes:meme_list')
    
    return render(request, 'memes/confirm_delete.html', {'meme': meme})


@login_required
def comment_edit(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    
    if comment.author != request.user:
        messages.error(request, 'У вас нет прав на редактирование этого комментария!')
        return redirect('memes:meme_detail', meme_id=comment.meme.id)
    
    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            messages.success(request, 'Комментарий обновлен!')
            return redirect('memes:meme_detail', meme_id=comment.meme.id)
    else:
        form = CommentForm(instance=comment)
    
    return render(request, 'memes/comment_form.html', {
        'form': form, 
        'comment': comment,
        'meme': comment.meme
    })


@login_required
def comment_delete(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    
    if comment.author != request.user:
        messages.error(request, 'У вас нет прав на удаление этого комментария!')
        return redirect('memes:meme_detail', meme_id=comment.meme.id)
    
    meme_id = comment.meme.id
    
    if request.method == 'POST':
        comment.delete()
        messages.success(request, 'Комментарий удален!')
        return redirect('memes:meme_detail', meme_id=meme_id)
    
    return render(request, 'memes/confirm_delete_comment.html', {'comment': comment})

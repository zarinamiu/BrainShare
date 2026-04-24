from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Community, CommunityMembership


def community_list(request):
    """Список всех сообществ"""
    communities = Community.objects.all()
    return render(request, 'communities/community_list.html', {
        'communities': communities
    })


@login_required
def community_create(request):
    """Создание нового сообщества"""
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        is_private = request.POST.get('is_private') == 'on'
        image = request.FILES.get('image')
        
        if name:
            community = Community.objects.create(
                name=name,
                description=description,
                creator=request.user,
                is_private=is_private
            )
            
            if image:
                community.image = image
                community.save()
            
            CommunityMembership.objects.create(
                community=community,
                user=request.user,
                role='admin'
            )
            messages.success(request, f'Сообщество "{name}" создано!')
            return redirect('communities:community_detail', community_id=community.pk)
        else:
            messages.error(request, 'Введите название сообщества')
    
    return render(request, 'communities/community_create.html')


def community_detail(request, community_id):
    """Страница сообщества"""
    community = get_object_or_404(Community, pk=community_id)
    is_member = False
    user_role = None
    
    if request.user.is_authenticated:
        try:
            membership = CommunityMembership.objects.get(
                community=community,
                user=request.user
            )
            is_member = True
            user_role = membership.role
        except CommunityMembership.DoesNotExist:
            pass
    
    return render(request, 'communities/community_detail.html', {
        'community': community,
        'is_member': is_member,
        'user_role': user_role
    })


@login_required
def community_join(request, community_id):
    """Вступление в сообщество"""
    community = get_object_or_404(Community, pk=community_id)
    
    if CommunityMembership.objects.filter(community=community, user=request.user).exists():
        messages.warning(request, 'Вы уже участник этого сообщества')
    else:
        CommunityMembership.objects.create(
            community=community,
            user=request.user,
            role='member'
        )
        messages.success(request, f'Вы вступили в сообщество "{community.name}"!')
    
    return redirect('communities:community_detail', community_id=community.pk)


@login_required
def community_leave(request, community_id):
    """Выход из сообщества"""
    community = get_object_or_404(Community, pk=community_id)
    
    try:
        membership = CommunityMembership.objects.get(
            community=community,
            user=request.user
        )
        membership.delete()
        messages.success(request, f'Вы вышли из сообщества "{community.name}"')
    except CommunityMembership.DoesNotExist:
        messages.warning(request, 'Вы не участник этого сообщества')
    
    return redirect('communities:community_list')

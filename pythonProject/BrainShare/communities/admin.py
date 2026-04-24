from django.contrib import admin
from .models import Community, CommunityMembership


@admin.register(Community)
class CommunityAdmin(admin.ModelAdmin):
    list_display = ('name', 'creator', 'created_at', 'is_private', 'members_count')
    list_filter = ('is_private', 'created_at')
    search_fields = ('name', 'description')
    date_hierarchy = 'created_at'
    raw_id_fields = ('creator',)


@admin.register(CommunityMembership)
class CommunityMembershipAdmin(admin.ModelAdmin):
    list_display = ('user', 'community', 'role', 'joined_at')
    list_filter = ('role', 'joined_at')
    search_fields = ('user__username', 'community__name')
    date_hierarchy = 'joined_at'

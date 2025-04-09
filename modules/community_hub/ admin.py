# modules/community_hub/admin.py
from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import (
    CommunityModel,
    CommunityMemberModel,
    CommunityEventModel,
    CommunityPostModel
)

class CommunityMemberInline(admin.TabularInline):
    """Inline для участников сообщества"""
    model = CommunityMemberModel
    extra = 0
    fields = ('user', 'role', 'contributions', 'last_active')
    readonly_fields = ('last_active',)

@admin.register(CommunityModel)
class CommunityAdmin(admin.ModelAdmin):
    """Админка для сообществ"""
    list_display = ('name', 'category', 'members_count', 'is_active')
    list_filter = ('category', 'is_public', 'is_active')
    search_fields = ('name', 'description')
    inlines = (CommunityMemberInline,)
    fieldsets = (
        (None, {
            'fields': ('name', 'description', 'creator')
        }),
        (_('Settings'), {
            'fields': ('category', 'is_public', 'rules')
        }),
        (_('Metadata'), {
            'fields': ('tags', 'location', 'avatar_url')
        }),
    )

@admin.register(CommunityEventModel)
class EventAdmin(admin.ModelAdmin):
    """Админка для мероприятий"""
    list_display = ('title', 'community', 'start_time', 'status')
    list_filter = ('status', 'is_online')
    date_hierarchy = 'start_time'
    raw_id_fields = ('community', 'organizer')
    search_fields = ('title', 'description')

@admin.register(CommunityPostModel)
class PostAdmin(admin.ModelAdmin):
    """Админка для публикаций"""
    list_display = ('title', 'author', 'community', 'status')
    list_filter = ('status', 'is_pinned')
    search_fields = ('title', 'content')
    raw_id_fields = ('author', 'community', 'moderator')
from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .infrastructure.models import (
    NewsArticleModel,
    NewsSubscriptionModel
)

class NewsArticleAdmin(admin.ModelAdmin):
    list_display = (
        'truncated_title',
        'category',
        'priority',
        'author',
        'views_count',
        'publish_status',
        'created_at'
    )
    list_filter = ('category', 'is_published', 'priority')
    search_fields = ('title', 'content', 'author__email')
    date_hierarchy = 'created_at'
    actions = ['publish_selected', 'unpublish_selected']
    readonly_fields = ('views_count', 'created_at', 'modified_at')
    fieldsets = (
        (_('Основная информация'), {
            'fields': ('title', 'content', 'author')
        }),
        (_('Классификация'), {
            'fields': ('category', 'priority', 'geo_location')
        }),
        (_('Метаданные'), {
            'fields': ('sources', 'media_attachments')
        }),
        (_('Публикация'), {
            'fields': ('is_published', 'publish_at')
        }),
        (_('Статистика'), {
            'fields': ('views_count', 'created_at', 'modified_at')
        }),
    )

    def truncated_title(self, obj):
        return obj.title[:50] + '...' if len(obj.title) > 50 else obj.title
    truncated_title.short_description = _('Заголовок')

    def publish_status(self, obj):
        return _('Опубликовано') if obj.is_published else _('Черновик')
    publish_status.short_description = _('Статус')

    @admin.action(description=_('Опубликовать выбранные статьи'))
    def publish_selected(self, request, queryset):
        updated = queryset.update(is_published=True)
        self.message_user(
            request,
            _('Опубликовано %(count)d статей') % {'count': updated}
        )

    @admin.action(description=_('Снять с публикации выбранные статьи'))
    def unpublish_selected(self, request, queryset):
        updated = queryset.update(is_published=False)
        self.message_user(
            request,
            _('Снято с публикации %(count)d статей') % {'count': updated}
        )

class NewsSubscriptionAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'categories_list',
        'notification_channels',
        'subscription_status',
        'created_at'
    )
    list_filter = ('is_active', 'preferred_language')
    search_fields = ('user__email', 'categories')
    actions = ['activate_subscriptions', 'deactivate_subscriptions']

    def categories_list(self, obj):
        return ", ".join(obj.categories)
    categories_list.short_description = _('Категории')

    def subscription_status(self, obj):
        return _('Активна') if obj.is_active else _('Неактивна')
    subscription_status.short_description = _('Статус')

    @admin.action(description=_('Активировать выбранные подписки'))
    def activate_subscriptions(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(
            request,
            _('Активировано %(count)d подписок') % {'count': updated}
        )

    @admin.action(description=_('Деактивировать выбранные подписки'))
    def deactivate_subscriptions(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(
            request,
            _('Деактивировано %(count)d подписок') % {'count': updated}
        )

admin.site.register(NewsArticleModel, NewsArticleAdmin)
admin.site.register(NewsSubscriptionModel, NewsSubscriptionAdmin)
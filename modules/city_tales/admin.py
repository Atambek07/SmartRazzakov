from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .models import Tale, TaleContent, UserPreferences, Location
from .forms import TaleAdminForm

@admin.register(Tale)
class TaleAdmin(admin.ModelAdmin):
    """Администрирование историй"""
    form = TaleAdminForm
    list_display = ('title', 'author', 'location_link', 'status_badge', 'created_at')
    list_filter = ('status', 'language', 'created_at')
    search_fields = ('title', 'author__username', 'location__name')
    readonly_fields = ('qr_code_preview',)
    fieldsets = (
        ('Основное', {
            'fields': ('title', 'author', 'location', 'language')
        }),
        ('Контент', {
            'fields': ('description', 'audio_file', 'text_content', 'images')
        }),
        ('Метаданные', {
            'fields': ('status', 'tags', 'qr_code_preview')
        }),
    )
    actions = ['approve_tales', 'export_as_json']

    def location_link(self, obj):
        if obj.location:
            url = reverse('admin:city_tales_location_change', args=[obj.location.id])
            return format_html('<a href="{}">{}</a>', url, obj.location.name)
        return "-"
    location_link.short_description = "Локация"

    def status_badge(self, obj):
        colors = {
            'draft': 'gray',
            'published': 'green',
            'archived': 'red'
        }
        return format_html(
            '<span style="color: white; background-color: {}; padding: 3px 6px; border-radius: 3px;">{}</span>',
            colors.get(obj.status, 'gray'),
            obj.get_status_display()
        )
    status_badge.short_description = "Статус"

    def qr_code_preview(self, obj):
        if obj.qr_code:
            return format_html('<img src="{}" height="100" />', obj.qr_code.url)
        return "-"
    qr_code_preview.short_description = "QR-код"

    @admin.action(description="Одобрить выбранные истории")
    def approve_tales(self, request, queryset):
        updated = queryset.update(status='published')
        self.message_user(request, f"{updated} историй одобрено")

    @admin.action(description="Экспортировать как JSON")
    def export_as_json(self, request, queryset):
        # Реализация экспорта
        pass

@admin.register(TaleContent)
class TaleContentAdmin(admin.ModelAdmin):
    """Управление мультимедийным контентом"""
    list_display = ('tale_title', 'content_type', 'language')
    list_select_related = ('tale',)

    def tale_title(self, obj):
        return obj.tale.title
    tale_title.short_description = "История"

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    """Администрирование локаций"""
    list_display = ('name', 'city', 'geo_link')
    search_fields = ('name', 'city', 'address')

    def geo_link(self, obj):
        if obj.latitude and obj.longitude:
            url = f"https://maps.google.com/?q={obj.latitude},{obj.longitude}"
            return format_html('<a href="{}" target="_blank">🌐 На карте</a>', url)
        return "-"
    geo_link.short_description = "Координаты"
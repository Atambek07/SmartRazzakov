from django.contrib import admin
from django.contrib.gis.admin import GISModelAdmin
from leaflet.admin import LeafletGeoAdmin  # Для улучшенного отображения карты
from .infrastructure.models import RouteModel, TrafficAlertModel, TransportModel

# Координаты центра Раззаков (примерные, уточните точные координаты)
DEFAULT_LONGITUDE = 72.3456  # Долгота Раззаков
DEFAULT_LATITUDE = 40.1234  # Широта Раззаков
DEFAULT_ZOOM = 13  # Масштаб карты по умолчанию


@admin.register(RouteModel)
class RouteAdmin(LeafletGeoAdmin):  # Используем Leaflet для красивого отображения
    list_display = ('id', 'transport_type', 'distance_km', 'start_address', 'end_address')
    search_fields = ('id', 'transport_type', 'start_address', 'end_address')
    list_filter = ('transport_type', 'created_at')
    readonly_fields = ('created_at', 'updated_at')

    # Настройки карты для Раззаков
    settings_overrides = {
        'DEFAULT_CENTER': (DEFAULT_LATITUDE, DEFAULT_LONGITUDE),
        'DEFAULT_ZOOM': DEFAULT_ZOOM,
        'SPATIAL_EXTENT': (72.1, 40.0, 72.5, 40.3),  # Границы карты (min_lon, min_lat, max_lon, max_lat)
        'TILES': [('OpenStreetMap', '//{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
                   {'attribution': '© OpenStreetMap contributors'})]
    }

    fieldsets = (
        ('Основная информация', {
            'fields': ('transport_type', 'distance_km')
        }),
        ('Геоданные', {
            'fields': ('start_point', 'end_point', 'waypoints'),
            'classes': ('wide', 'extrapretty')
        }),
        ('Дополнительно', {
            'fields': ('start_address', 'end_address', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )


@admin.register(TrafficAlertModel)
class TrafficAlertAdmin(LeafletGeoAdmin):
    list_display = ('id', 'message', 'radius_km', 'location', 'severity', 'is_active')
    list_editable = ('severity', 'is_active')
    list_filter = ('severity', 'is_active', 'created_at')

    # Настройки карты
    settings_overrides = {
        'DEFAULT_CENTER': (DEFAULT_LATITUDE, DEFAULT_LONGITUDE),
        'DEFAULT_ZOOM': 14,
        'TILES': [('Transport Map', '//{s}.tile.thunderforest.com/transport/{z}/{x}/{y}.png',
                   {'attribution': '© Thunderforest'})]
    }

    actions = ['activate_alerts', 'deactivate_alerts']

    def activate_alerts(self, request, queryset):
        queryset.update(is_active=True)

    activate_alerts.short_description = "Активировать выбранные алерты"

    def deactivate_alerts(self, request, queryset):
        queryset.update(is_active=False)

    deactivate_alerts.short_description = "Деактивировать выбранные алерты"


@admin.register(TransportModel)
class TransportAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'speed_kmh', 'eco_score', 'is_available')
    list_editable = ('speed_kmh', 'eco_score', 'is_available')
    list_filter = ('is_available',)
    search_fields = ('name',)

    fieldsets = (
        (None, {
            'fields': ('name', 'icon')
        }),
        ('Характеристики', {
            'fields': ('speed_kmh', 'eco_score', 'capacity')
        }),
        ('Доступность', {
            'fields': ('is_available', 'operating_hours')
        })
    )


# Кастомизация админ-панели под Раззаков
admin.site.site_header = "Smart Раззаков: Управление маршрутами"
admin.site.index_title = "Цифровая платформа города"
admin.site.site_title = "Администрирование CityRoutes"
from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

class CityRoutesConfig(AppConfig):
    """Конфигурация приложения CityRoutes"""
    
    # Стандартные параметры
    name = 'city_routes'
    verbose_name = _('Маршруты города')
    
    # Дополнительные настройки
    default_auto_field = 'django.db.models.BigAutoField'
    cache_timeout = 3600  # Время кеширования в секундах
    
    def ready(self):
        """Инициализация приложения"""
        # Импорт сигналов и задач Celery (если есть)
        try:
            from . import signals  # noqa
            from . import tasks    # noqa
        except ImportError:
            pass
        
        # Подключение административных модулей
        self._setup_admin()
        
        # Инициализация кеша маршрутов
        self._init_route_cache()
    
    def _setup_admin(self):
        """Кастомизация админки"""
        from django.contrib import admin
        from .admin import custom_admin_site
        
        # Переопределяем стандартную админку
        admin.site = custom_admin_site
        admin.sites.site = custom_admin_site
    
    def _init_route_cache(self):
        """Инициализация кеша маршрутов"""
        from django.core.cache import cache
        from .models import Route
        
        if not cache.get('routes_initialized'):
            # Предзагрузка популярных маршрутов
            popular_routes = Route.objects.filter(is_popular=True)[:10]
            cache.set('popular_routes', popular_routes, self.cache_timeout)
            cache.set('routes_initialized', True, None)
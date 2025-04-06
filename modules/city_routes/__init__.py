"""
Модуль инициализации приложения CityRoutes

Экспортирует основные компоненты:
- Конфигурацию приложения (default_app_config)
- Версию API
- Основные константы
"""

import os
from django.conf import settings

# Настройки по умолчанию
default_app_config = 'city_routes.apps.CityRoutesConfig'

# Версия API
API_VERSION = '1.0.0'

# Константы приложения
MAX_ROUTE_LENGTH_KM = 50.0
DEFAULT_CITY_CENTER = (43.2384, 76.9454)  # Координаты Раззакова

def configure_settings():
    """Динамическая настройка параметров"""
    if not hasattr(settings, 'CITY_ROUTES_CONFIG'):
        settings.CITY_ROUTES_CONFIG = {
            'MAP_PROVIDER': 'osm',
            'CACHE_ENABLED': True,
            'DEFAULT_LANGUAGE': 'ru'
        }

# Автоматическая настройка при импорте
configure_settings()

# Импорт основных компонентов
from .routes import *  # noqa
from .services import *  # noqa
from .exceptions import *  # noqa

__all__ = [
    'API_VERSION',
    'MAX_ROUTE_LENGTH_KM',
    'DEFAULT_CITY_CENTER'
]

# Логирование инициализации
if not os.environ.get('DJANGO_SETUP_COMPLETE'):
    print(f'CityRoutes {API_VERSION} initialized')  # pragma: no cover
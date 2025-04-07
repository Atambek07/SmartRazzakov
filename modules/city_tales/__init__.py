# Регистрация конфигурации приложения по умолчанию
default_app_config = 'city_tales.apps.CityTalesConfig'

# Экспорт основных моделей для удобного импорта
from .models import (  # noqa
    Tale,
    TaleContent,
    Location,
    UserPreferences
)

__version__ = '1.0.0'
__author__ = 'Your Team'
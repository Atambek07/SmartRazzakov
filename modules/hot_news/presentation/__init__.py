"""
Презентационный слой модуля HotNews

Содержит:
- Маршруты API
- Сериализаторы
- Представления
- Конфигурацию Swagger
"""

# Экспорт основных компонентов для упрощения импорта
from .urls import urlpatterns as hot_news_urls
from .serializers import *
from .views import *

__all__ = [
    'hot_news_urls',
    'NewsCreateSerializer',
    'NewsResponseSerializer',
    'SubscriptionSerializer',
    'EmergencyAPIView'
]
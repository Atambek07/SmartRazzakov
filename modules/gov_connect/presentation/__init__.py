# modules/gov_connect/presentation/__init__.py
"""
Презентационный слой модуля GovConnect

Экспортирует:
- Основной роутер API
- Сериализаторы
- Представления
"""
from .urls import router as govconnect_router
from .serializers import *
from .views import *

__all__ = [
    'govconnect_router',
    'serializers',
    'views'
]
# modules/feedback/__init__.py
"""
Главный модуль для работы с отзывами и рейтингами

Экспортирует основные компоненты:
- Модели данных
- API views и сериализаторы
- Сервисы и репозитории
"""

from .apps import FeedbackConfig
from .admin import *  # noqa

default_app_config = 'modules.feedback.apps.FeedbackConfig'

__all__ = [
    'FeedbackConfig',
    'ReviewMapper',
    'RatingMapper'
]
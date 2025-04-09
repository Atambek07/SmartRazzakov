# modules/feedback/domain/__init__.py
"""
Главный файл доменного слоя Feedback модуля

Экспортирует:
- Базовые сущности предметной области
- Специализированные исключения
- Интерфейсы сервисов
"""

from .entities import *
from .exceptions import *
from .services import *

__all__ = [
    'ReviewEntity',
    'RatingSummary',
    'FeedbackException',
    'DuplicateReviewError',
    'InvalidRatingError',
    'ReviewNotFoundError',
    'ModerationError',
    'BaseRatingService',
    'BaseReviewService',
    'BaseSentimentAnalyzer'
]
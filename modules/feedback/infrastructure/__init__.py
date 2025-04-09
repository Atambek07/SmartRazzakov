# modules/feedback/infrastructure/__init__.py
"""
Инфраструктурный слой модуля Feedback

Экспортирует:
- Модели данных
- Репозитории для работы с БД
- Интеграции с внешними сервисами
- Вспомогательные инструменты
"""

from .models import (
    Review,
    ReviewImage,
    ReviewTag,
    RatingSnapshot,
    ReviewVote
)

from .repositories import (
    DjangoReviewRepository,
    DjangoRatingRepository,
    ReviewQuerySet,
    RatingQuerySet
)

from .integrations import (
    AIModerationService,
    ManualModerationAdapter,
    ProfanityFilter,
    SpamDetector,
    EmailNotifier,
    PushNotifier,
    SMSNotifier
)

__all__ = [
    # Models
    'Review',
    'ReviewImage',
    'ReviewTag',
    'RatingSnapshot',
    'ReviewVote',
    
    # Repositories
    'DjangoReviewRepository',
    'DjangoRatingRepository',
    'ReviewQuerySet',
    'RatingQuerySet',
    
    # Moderation
    'AIModerationService',
    'ManualModerationAdapter',
    'ProfanityFilter',
    'SpamDetector',
    
    # Notifications
    'EmailNotifier',
    'PushNotifier',
    'SMSNotifier'
]

# Инициализация интеграций по умолчанию
default_moderator = AIModerationService()
default_notifier = EmailNotifier()

def get_default_moderator():
    return default_moderator

def get_default_notifier():
    return default_notifier
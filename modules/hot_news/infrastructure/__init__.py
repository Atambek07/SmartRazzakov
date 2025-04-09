"""
Инфраструктурный слой модуля HotNews
"""

# Репозитории
from .repositories import (
    NewsRepository,
    SubscriptionRepository
)

# Модели данных
from .models import (
    NewsArticleModel,
    NewsSubscriptionModel
)

# Интеграции
from .integrations.rss import (
    RSSFeedManager,
    RSSParser,
    RSSSource
)

# Уведомления
from .notifications import (
    PushNotifier,
    SMSNotifier
)

# Экспорт основных компонентов
__all__ = [
    'NewsRepository',
    'SubscriptionRepository',
    'NewsArticleModel',
    'NewsSubscriptionModel',
    'RSSFeedManager',
    'RSSParser',
    'RSSSource',
    'PushNotifier',
    'SMSNotifier'
]
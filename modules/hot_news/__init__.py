"""
Модуль HotNews - управление новостями, подписками и экстренными оповещениями

Экспортирует основные компоненты:
- Модели: NewsArticle, NewsSubscription
- Сервисы: NewsService, SubscriptionService
- API Views: NewsAPIView, SubscriptionAPIView
"""

# Экспорт основных компонентов для удобства
from .infrastructure.models import (
    NewsArticleModel as NewsArticle,
    NewsSubscriptionModel as NewsSubscription
)
from .application.use_cases import (
    NewsManagementUseCase as NewsService,
    SubscriptionManagementUseCase as SubscriptionService
)
from .presentation.views import (
    NewsAPIView,
    NewsDetailAPIView,
    SubscriptionAPIView,
    EmergencyAPIView
)

__all__ = [
    'NewsArticle',
    'NewsSubscription',
    'NewsService',
    'SubscriptionService',
    'NewsAPIView',
    'NewsDetailAPIView',
    'SubscriptionAPIView',
    'EmergencyAPIView'
]
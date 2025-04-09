# modules/feedback/presentation/__init__.py
"""
Presentation Layer модуля Feedback

Экспортирует основные компоненты для работы с API:
- Сериализаторы для преобразования данных
- Представления (API endpoints)
- URL-маршруты
- Вспомогательные компоненты
"""

from .urls import urlpatterns as feedback_urls
from .serializers import (
    ReviewCreateSerializer,
    ReviewResponseSerializer,
    RatingSummarySerializer,
    ReviewVoteSerializer
)
from .views import (
    ReviewListCreateView,
    ReviewDetailView,
    RatingSummaryView,
    ReviewVoteView,
    ModerationQueueView,
    ModerationActionView
)

__all__ = [
    # URL Patterns
    'feedback_urls',
    
    # Serializers
    'ReviewCreateSerializer',
    'ReviewResponseSerializer',
    'RatingSummarySerializer',
    'ReviewVoteSerializer',
    
    # Views
    'ReviewListCreateView',
    'ReviewDetailView',
    'RatingSummaryView',
    'ReviewVoteView',
    'ModerationQueueView',
    'ModerationActionView',
    
    # Permissions (если есть)
]

def get_feedback_urls():
    """Хелпер для получения URL-конфигурации модуля"""
    return feedback_urls
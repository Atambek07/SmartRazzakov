# modules/community_hub/domain/__init__.py
from .entities import (
    Community,
    CommunityMember,
    CommunityEvent,
    CommunityPost,
    CommunityCategory,
    MemberRole,
    EventStatus,
    PostStatus
)
from .exceptions import (
    CommunityHubException,
    CommunityNotFoundError,
    MemberNotFoundError,
    PermissionDeniedError,
    BusinessRuleValidationError,
    EventValidationError,
    ContentModerationError
)

# Реэкспорт основных сущностей и исключений
__all__ = [
    'Community',
    'CommunityMember',
    'CommunityEvent',
    'CommunityPost',
    'CommunityCategory',
    'MemberRole',
    'EventStatus',
    'PostStatus',
    'CommunityHubException',
    'CommunityNotFoundError',
    'MemberNotFoundError',
    'PermissionDeniedError',
    'BusinessRuleValidationError',
    'EventValidationError',
    'ContentModerationError'
]

# Дополнительные доменные сервисы
class CommunityRulesValidator:
    """Валидатор бизнес-правил сообщества"""
    @staticmethod
    def validate_community_name(name: str) -> bool:
        return 3 <= len(name) <= 100 and any(c.isalpha() for c in name)

    @staticmethod
    def validate_member_limit(current: int, max_limit: int) -> bool:
        return current < max_limit

class EventScheduler:
    """Доменный сервис для работы с расписанием мероприятий"""
    @staticmethod
    def is_valid_time_range(start: datetime, end: datetime) -> bool:
        return end > start

    @staticmethod
    def is_upcoming(event: 'CommunityEvent') -> bool:
        return event.status == EventStatus.PLANNED and event.start_time > datetime.utcnow()
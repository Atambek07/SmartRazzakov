# modules/community_hub/domain/exceptions.py
class CommunityHubException(Exception):
    """Базовое исключение для домена CommunityHub"""
    def __init__(self, message: str, code: str = None):
        self.code = code
        self.message = message
        super().__init__(message)

class CommunityNotFoundError(CommunityHubException):
    """Сообщество не найдено"""
    def __init__(self, community_id: str = None):
        message = f"Community not found{f': {community_id}' if community_id else ''}"
        super().__init__(message, code="community_not_found")

class MemberNotFoundError(CommunityHubException):
    """Участник не найден"""
    def __init__(self, user_id: str, community_id: str):
        message = f"User {user_id} not member of community {community_id}"
        super().__init__(message, code="member_not_found")

class PermissionDeniedError(CommunityHubException):
    """Недостаточно прав"""
    def __init__(self, action: str, required_role: str = None):
        message = f"Permission denied for action: {action}"
        if required_role:
            message += f", requires role: {required_role}"
        super().__init__(message, code="permission_denied")

class BusinessRuleValidationError(CommunityHubException):
    """Нарушение бизнес-правил"""
    def __init__(self, rule: str, details: str = None):
        message = f"Business rule violation: {rule}"
        if details:
            message += f" ({details})"
        super().__init__(message, code="business_rule_violation")

class EventValidationError(CommunityHubException):
    """Ошибка валидации мероприятия"""
    def __init__(self, field: str, reason: str):
        message = f"Invalid event {field}: {reason}"
        super().__init__(message, code="event_validation_error")

class ContentModerationError(CommunityHubException):
    """Ошибка модерации контента"""
    def __init__(self, content_id: str, reason: str):
        message = f"Content moderation failed for {content_id}: {reason}"
        super().__init__(message, code="content_moderation_failed")
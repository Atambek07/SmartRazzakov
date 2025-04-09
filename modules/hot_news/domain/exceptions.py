class NewsException(Exception):
    """Базовое исключение для новостного модуля"""
    def __init__(self, message: str, code: str = "NEWS_ERROR"):
        self.code = code
        self.message = message
        super().__init__(message)

class NewsValidationError(NewsException):
    def __init__(self, message: str):
        super().__init__(message=message, code="NEWS_VALIDATION_ERROR")

class NewsNotFoundError(NewsException):
    def __init__(self, article_id: str = None):
        message = "News article not found"
        if article_id:
            message += f": {article_id}"
        super().__init__(message=message, code="NEWS_NOT_FOUND")

class SubscriptionNotFoundError(NewsException):
    def __init__(self, subscription_id: str = None):
        message = "Subscription not found"
        if subscription_id:
            message += f": {subscription_id}"
        super().__init__(message=message, code="SUBSCRIPTION_NOT_FOUND")

class NewsPublishingError(NewsException):
    def __init__(self, reason: str):
        super().__init__(
            message=f"News publishing failed: {reason}",
            code="PUBLISHING_ERROR"
        )

class EmergencyProtocolViolation(NewsException):
    def __init__(self, protocol: str):
        super().__init__(
            message=f"Emergency protocol violation: {protocol}",
            code="EMERGENCY_PROTOCOL_ERROR"
        )

class NewsRateLimitExceeded(NewsException):
    def __init__(self, limit: int):
        super().__init__(
            message=f"News rate limit exceeded ({limit}/hour)",
            code="RATE_LIMIT_EXCEEDED"
        )
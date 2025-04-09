# modules/feedback/domain/exceptions.py
class FeedbackException(Exception):
    """Базовое исключение для модуля Feedback"""
    code = "feedback_error"
    message = "Ошибка в работе с отзывами"

class DuplicateReviewError(FeedbackException):
    code = "duplicate_review"
    message = "Вы уже оставляли отзыв для этого объекта"

class InvalidRatingError(FeedbackException):
    code = "invalid_rating"
    message = "Некорректное значение оценки"

class ReviewNotFoundError(FeedbackException):
    code = "review_not_found"
    message = "Запрошенный отзыв не найден"

class ModerationError(FeedbackException):
    code = "moderation_failed"
    message = "Ошибка при модерации отзыва"

class ReviewValidationError(FeedbackException):
    code = "invalid_review_content"
    message = "Отзыв содержит недопустимый контент"

class PermissionDeniedError(FeedbackException):
    code = "permission_denied"
    message = "Недостаточно прав для выполнения операции"
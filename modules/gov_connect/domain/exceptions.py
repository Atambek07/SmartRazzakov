# modules/gov_connect/domain/exceptions.py
"""
Кастомные исключения доменного уровня для GovConnect
"""

class GovConnectError(Exception):
    """Базовое исключение для всех ошибок модуля"""
    code: str = "GOV_CONNECT_ERROR"
    message: str = "Ошибка в модуле GovConnect"

    def __init__(self, context: dict = None):
        self.context = context or {}

class InvalidGeoDataError(GovConnectError):
    code = "INVALID_GEO_DATA"
    message = "Некорректные геоданные"

class ComplaintNotFoundError(GovConnectError):
    code = "COMPLAINT_NOT_FOUND"
    message = "Жалоба не найдена"

class BookingConflictError(GovConnectError):
    code = "BOOKING_CONFLICT"
    message = "Конфликт времени бронирования"

class VotingPermissionError(GovConnectError):
    code = "VOTING_PERMISSION_DENIED"
    message = "Нет прав для участия в голосовании"

class WorkflowTransitionError(GovConnectError):
    code = "INVALID_WORKFLOW_TRANSITION"
    message = "Недопустимое изменение статуса"

class DocumentValidationError(GovConnectError):
    code = "DOCUMENT_VALIDATION_FAILED"
    message = "Ошибка валидации документа"
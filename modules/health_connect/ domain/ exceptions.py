# modules/health_connect/domain/exceptions.py
class HealthConnectException(Exception):
    """Базовое исключение для модуля HealthConnect"""
    def __init__(self, detail: str = None):
        self.detail = detail or "Произошла ошибка в модуле HealthConnect"
        super().__init__(self.detail)

class MedicalRecordNotFound(HealthConnectException):
    def __init__(self, record_id: str = None):
        detail = f"Медицинская запись {record_id} не найдена" if record_id else "Медицинская запись не найдена"
        super().__init__(detail)

class AppointmentConflict(HealthConnectException):
    def __init__(self, time: str = None):
        detail = f"Конфликт времени записи: {time}" if time else "Конфликт времени записи"
        super().__init__(detail)

class ProviderNotAvailable(HealthConnectException):
    def __init__(self, provider_id: str = None):
        detail = f"Врач {provider_id} недоступен" if provider_id else "Врач недоступен"
        super().__init__(detail)

class PermissionDenied(HealthConnectException):
    def __init__(self, action: str = None):
        detail = f"Нет прав для выполнения действия: {action}" if action else "Доступ запрещен"
        super().__init__(detail)

class InvalidMedicalData(HealthConnectException):
    def __init__(self, field: str = None):
        detail = f"Некорректные данные в поле: {field}" if field else "Некорректные медицинские данные"
        super().__init__(detail)

class TelemedicineException(HealthConnectException):
    def __init__(self, reason: str = None):
        detail = f"Ошибка телемедицины: {reason}" if reason else "Ошибка телемедицинского сервиса"
        super().__init__(detail)
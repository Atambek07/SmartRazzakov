class TaleNotFoundError(Exception):
    """Ошибка при отсутствии контента."""
    def __init__(self, qr_code: str):
        self.qr_code = qr_code
        super().__init__(
            f"Контент для QR-кода {qr_code} не найден. "
            "Проверьте правильность кода или обратитесь в поддержку."
        )

class InvalidContentFormatError(Exception):
    """Ошибка несовместимого формата."""
    def __init__(self, current_format: str, allowed_formats: list):
        super().__init__(
            f"Формат {current_format} не поддерживается. "
            f"Доступные варианты: {', '.join(allowed_formats)}"
        )

class UserPreferencesNotFoundError(Exception):
    """Ошибка отсутствия настроек пользователя."""
    def __init__(self, user_id: str):
        super().__init__(
            f"Настройки для пользователя {user_id} не найдены. "
            "Пожалуйста, установите предпочтения в личном кабинете."
        )

class ContentModerationError(Exception):
    """Ошибка модерации контента."""
    def __init__(self, tale_id: str, reason: str):
        super().__init__(
            f"Контент {tale_id} не прошел модерацию. Причина: {reason}"
        )
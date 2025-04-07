from dataclasses import dataclass
from typing import List, Optional, Dict, Any
from enum import Enum
import uuid

class ContentFormat(str, Enum):
    """Форматы доступного контента."""
    AUDIO = "audio"
    TEXT = "text"
    VISUAL = "visual"  # Инфографика, схемы, фото

@dataclass
class TaleContent:
    """
    Сущность контента для достопримечательности.
    Содержит мультиформатные данные и метаинформацию.
    """
    id: str = str(uuid.uuid4())  # Уникальный UUID
    title: str
    location_id: str  # Связь с достопримечательностью
    author_id: str  # ID создателя контента (краеведа, жителя)
    audio_url: Optional[str] = None  # Путь к аудиофайлу (S3 или локальный)
    text_content: Optional[str] = None  # Текстовая расшифровка
    images: List[str] = None  # Список URL изображений
    qr_code: str = None  # Уникальный QR-идентификатор
    language: str = "ru"  # Язык контента
    duration_minutes: Optional[float] = None  # Для аудио/видео
    is_approved: bool = False  # Прошел ли модерацию
    created_at: str = None  # Дата создания (ISO format)
    updated_at: str = None  # Дата обновления

    def __post_init__(self):
        if self.images is None:
            self.images = []
        if not self.qr_code:
            self.qr_code = f"TALE_{self.id[:8]}"
        if not self.created_at:
            self.created_at = datetime.now().isoformat()
        if not self.updated_at:
            self.updated_at = self.created_at

    def validate(self):
        """Проверка целостности данных."""
        if not any([self.audio_url, self.text_content, self.images]):
            raise ValueError("Контент должен содержать хотя бы один формат")
        if self.audio_url and not self.duration_minutes:
            raise ValueError("Для аудио обязательна длительность")

@dataclass
class UserPreferences:
    """Настройки пользователя для персонализации контента."""
    user_id: str
    preferred_format: ContentFormat
    preferred_language: str = "ru"
    last_used_qr: Optional[str] = None  # Последний отсканированный QR
    font_size: int = 16  # Для текстового формата
    high_contrast: bool = False  # Для слабовидящих

    def update_format(self, new_format: ContentFormat):
        """Обновление предпочтений с валидацией."""
        if new_format not in ContentFormat:
            raise ValueError(f"Недопустимый формат: {new_format}")
        self.preferred_format = new_format
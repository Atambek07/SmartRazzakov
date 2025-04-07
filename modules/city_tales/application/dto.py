from dataclasses import dataclass
from enum import Enum
from typing import Optional, List

class ContentFormat(str, Enum):
    AUDIO = "audio"
    TEXT = "text"
    VISUAL = "visual"  # Для инфографики/схем

@dataclass
class TaleContentDTO:
    id: str
    title: str
    location_id: str  # ID достопримечательности
    audio_url: Optional[str] = None
    text_content: Optional[str] = None
    images: List[str] = None  # Список URL изображений/схем
    format_preference: Optional[ContentFormat] = None  # Предпочтение пользователя

@dataclass
class QRRequestDTO:
    qr_code: str  # Уникальный ID QR-кода
    user_id: Optional[str] = None  # Для персонализации

@dataclass
class UserPreferenceDTO:
    user_id: str
    preferred_format: ContentFormat
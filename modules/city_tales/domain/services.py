from .entities import ContentFormat, TaleContent, UserPreferences
from .exceptions import (
    InvalidContentFormatError,
    TaleNotFoundError,
    UserPreferencesNotFoundError
)
from typing import Optional, List
import logging

logger = logging.getLogger(__name__)

class ContentFormatService:
    """Сервис управления форматами контента."""

    @staticmethod
    def determine_format(
        tale: TaleContent,
        user_preference: Optional[ContentFormat] = None,
        device_type: Optional[str] = None
    ) -> ContentFormat:
        """
        Определяет оптимальный формат контента на основе:
        1. Предпочтений пользователя
        2. Возможностей устройства (мобильное/десктоп)
        3. Доступных форматов в контенте
        """
        available_formats = []
        if tale.audio_url:
            available_formats.append(ContentFormat.AUDIO)
        if tale.text_content or tale.images:
            available_formats.append(ContentFormat.TEXT)
            available_formats.append(ContentFormat.VISUAL)

        if not available_formats:
            raise TaleNotFoundError(tale.qr_code)

        # Приоритет: пользовательский выбор > устройство > дефолт
        if user_preference and user_preference in available_formats:
            logger.info(f"Используется предпочтение пользователя: {user_preference}")
            return user_preference

        # Автовыбор для устройств
        if device_type == "mobile":
            return ContentFormat.AUDIO if ContentFormat.AUDIO in available_formats else available_formats[0]
        else:
            return ContentFormat.VISUAL if ContentFormat.VISUAL in available_formats else available_formats[0]

    @staticmethod
    def validate_content(tale: TaleContent):
        """Проверка целостности контента."""
        tale.validate()
        if not tale.is_approved:
            raise ContentModerationError(tale.id, "Контент не прошел модерацию")

class GamificationService:
    """Сервис геймификации и достижений."""

    def __init__(self, points_per_tale: int = 10):
        self.points_per_tale = points_per_tale

    def calculate_rewards(
        self,
        user_id: str,
        tales_consumed: List[TaleContent]
    ) -> Dict[str, Any]:
        """Начисляет баллы и проверяет достижения."""
        total = len(tales_consumed)
        points = total * self.points_per_tale
        rewards = []

        if total >= 10:
            rewards.append({"name": "Историк", "reward": "3D-макет памятника"})
        if total >= 5:
            rewards.append({"name": "Любознательный", "reward": "Эксклюзивная книга"})

        return {
            "user_id": user_id,
            "total_points": points,
            "unlocked_rewards": rewards,
            "next_milestone": max(0, 10 - total) if total < 10 else None
        }
    
# domain/services.py
class GamificationEngine:
    """Движок геймификации"""
    def check_achievements(self, user_id: str):
        """Проверка достижений пользователя"""
    
    def award_points(self, user_id: str, action_type: str):
        """Начисление баллов за действия"""

class StoryCollector:
    """Система коллекционирования историй"""
    def get_collection_progress(self, user_id: str):
        """Прогресс по коллекциям"""
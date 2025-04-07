from typing import Optional, List
from django.core.exceptions import ObjectDoesNotExist
from .models import TaleContentModel, UserPreferencesModel
from domain.entities import TaleContent, UserPreferences
from domain.exceptions import TaleNotFoundError, UserPreferencesNotFoundError
import logging

logger = logging.getLogger(__name__)

class TaleRepository:
    """Репозиторий для работы с контентом историй."""

    def find_by_qr(self, qr_code: str) -> Optional[TaleContent]:
        try:
            model = TaleContentModel.objects.get(qr_code=qr_code)
            return self._to_entity(model)
        except ObjectDoesNotExist:
            logger.warning(f"QR-код не найден: {qr_code}")
            raise TaleNotFoundError(qr_code)

    def find_by_location(self, location_id: str) -> List[TaleContent]:
        return [
            self._to_entity(model)
            for model in TaleContentModel.objects.filter(location_id=location_id)
        ]

    def _to_entity(self, model: TaleContentModel) -> TaleContent:
        return TaleContent(
            id=str(model.id),
            title=model.title,
            location_id=model.location_id,
            author_id=model.author_id,
            audio_url=model.audio_url,
            text_content=model.text_content,
            images=model.images,
            qr_code=model.qr_code,
            language=model.language,
            duration_minutes=model.duration_minutes,
            is_approved=model.is_approved,
            created_at=model.created_at.isoformat(),
            updated_at=model.updated_at.isoformat()
        )

class UserPreferencesRepository:
    """Репозиторий для работы с настройками пользователей."""

    def get_preferences(self, user_id: str) -> UserPreferences:
        try:
            model = UserPreferencesModel.objects.get(user_id=user_id)
            return UserPreferences(
                user_id=model.user_id,
                preferred_format=model.preferred_format,
                preferred_language=model.preferred_language,
                last_used_qr=model.last_used_qr,
                font_size=model.font_size,
                high_contrast=model.high_contrast
            )
        except ObjectDoesNotExist:
            logger.error(f"Настройки не найдены для user_id: {user_id}")
            raise UserPreferencesNotFoundError(user_id)

    def update_preferences(self, user_id: str, preferred_format: str):
        UserPreferencesModel.objects.update_or_create(
            user_id=user_id,
            defaults={"preferred_format": preferred_format}
        )
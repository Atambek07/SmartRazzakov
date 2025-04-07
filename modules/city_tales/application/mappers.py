from . import dto
from domain.entities import TaleContent, UserPreferences

def map_tale_to_dto(tale: TaleContent, preference: dto.ContentFormat = None) -> dto.TaleContentDTO:
    """Конвертирует доменную сущность в DTO для API."""
    return dto.TaleContentDTO(
        id=str(tale.id),
        title=tale.title,
        location_id=tale.location_id,
        audio_url=tale.audio_url,
        text_content=tale.text_content,
        images=tale.images or [],
        format_preference=preference
    )

def map_preference_to_dto(prefs: UserPreferences) -> dto.UserPreferenceDTO:
    """Конвертирует настройки пользователя в DTO."""
    return dto.UserPreferenceDTO(
        user_id=str(prefs.user_id),
        preferred_format=dto.ContentFormat(prefs.preferred_format)
    )
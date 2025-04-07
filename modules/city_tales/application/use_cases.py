from typing import Optional
from . import dto
from domain.entities import TaleContent
from domain.exceptions import TaleNotFoundError
from domain.services import ContentFormatService
from infrastructure.repositories import TaleRepository, UserPreferencesRepository

class GetTaleContentUseCase:
    def __init__(
        self,
        tale_repo: TaleRepository,
        prefs_repo: UserPreferencesRepository,
        format_service: ContentFormatService
    ):
        self.tale_repo = tale_repo
        self.prefs_repo = prefs_repo
        self.format_service = format_service

    def execute(self, request: dto.QRRequestDTO) -> dto.TaleContentDTO:
        # 1. Найти контент по QR
        tale = self.tale_repo.find_by_qr(request.qr_code)
        if not tale:
            raise TaleNotFoundError(f"QR {request.qr_code} не найден")

        # 2. Получить предпочтения пользователя (если есть)
        user_prefs = None
        if request.user_id:
            user_prefs = self.prefs_repo.get_preferences(request.user_id)

        # 3. Определить формат контента
        preferred_format = self.format_service.determine_format(
            tale, 
            user_prefs.preferred_format if user_prefs else None
        )

        return dto.TaleContentDTO(
            id=str(tale.id),
            title=tale.title,
            location_id=tale.location_id,
            audio_url=tale.audio_url if preferred_format == dto.ContentFormat.AUDIO else None,
            text_content=tale.text_content if preferred_format == dto.ContentFormat.TEXT else None,
            images=tale.images if preferred_format == dto.ContentFormat.VISUAL else [],
            format_preference=preferred_format
        )

class UpdateUserPreferenceUseCase:
    def __init__(self, prefs_repo: UserPreferencesRepository):
        self.prefs_repo = prefs_repo

    def execute(self, request: dto.UserPreferenceDTO):
        self.prefs_repo.update_preferences(
            user_id=request.user_id,
            preferred_format=request.preferred_format.value
        )

class ContentEnhancementUseCase:
    """Улучшение контента AI"""
    def add_audio_transcription(self, tale_id: str):
        """Автоматическая транскрипция аудио в текст"""
    
    def generate_accessibility_version(self, tale_id: str):
        """Создание версий для слабовидящих/слабослышащих"""

class ContentTranslationUseCase:
    """Перевод контента на другие языки"""
    def translate_tale(self, tale_id: str, target_lang: str):
        """Перевод истории с сохранением в БД"""
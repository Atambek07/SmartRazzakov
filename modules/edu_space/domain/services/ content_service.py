from .entities import EducationalContent, ContentType
from .exceptions import InvalidContentError


class ContentValidator:
    @staticmethod
    def validate(content_data: dict) -> ContentType:
        """Проверяет корректность образовательного контента"""
        if not content_data.get('source'):
            raise InvalidContentError("Content source is required")

        if content_data['type'] == 'video' and not content_data.get('duration'):
            raise InvalidContentError("Video content requires duration")

        return ContentType(content_data['type'])


class ContentService:
    def create_content(self, content_data: dict, author_id: str) -> EducationalContent:
        """Создает новый образовательный материал"""
        content_type = ContentValidator.validate(content_data)

        return EducationalContent(
            id=None,
            title=content_data['title'],
            content_type=content_type,
            difficulty=content_data.get('difficulty', DifficultyLevel.BEGINNER),
            subject=content_data['subject'],
            author_id=author_id,
            created_at=datetime.now(),
            metadata=content_data.get('metadata', {})
        )
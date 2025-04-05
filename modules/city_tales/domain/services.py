from .entities import Story, ContentType
from .exceptions import InvalidContentError


class StoryService:
    @staticmethod
    def validate_content(content: dict) -> ContentType:
        """Определяет тип контента и проверяет его валидность"""
        has_text = bool(content.get('text'))
        has_audio = bool(content.get('audio'))

        if not has_text and not has_audio:
            raise InvalidContentError("Контент должен содержать текст или аудио")

        return ContentType.MIXED if has_text and has_audio else (
            ContentType.TEXT if has_text else ContentType.AUDIO
        )

    def create_story(self, title: str, content: dict, location: str, author_id: int) -> Story:
        """Создает новую историю"""
        content_type = self.validate_content(content)

        return Story(
            id=None,  # Будет присвоен при сохранении
            title=title,
            content=content,
            content_type=content_type,
            location=location,
            author_id=author_id,
            created_at=datetime.now()
        )
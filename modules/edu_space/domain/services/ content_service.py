from abc import ABC, abstractmethod
from uuid import UUID
from ..entities import EducationalContent
from ..exceptions import ContentValidationError, ContentPublishingError

class ContentService(ABC):
    @abstractmethod
    def upload_content(self, content_data: dict) -> EducationalContent:
        """Загружает новый образовательный контент"""
        pass

    @abstractmethod
    def publish_content(self, content_id: UUID):
        """Публикует контент для общего доступа"""
        pass

    @abstractmethod
    def generate_interactive_test(self, content_id: UUID) -> dict:
        """Генерирует интерактивный тест на основе контента"""
        pass

class BaseContentService(ContentService):
    def __init__(self, content_repository):
        self.content_repo = content_repository

    def publish_content(self, content_id: UUID):
        content = self.content_repo.get_by_id(content_id)
        
        if not content.file_url:
            raise ContentPublishingError("Content must have a file to publish")
            
        if content.is_published:
            raise ContentPublishingError("Content already published")
            
        content.is_published = True
        return self.content_repo.save(content)
from .domain.services import StoryService
from .infrastructure.repositories import StoryRepository
from .dto import CreateStoryDTO


class CreateStoryUseCase:
    def __init__(self, repository: StoryRepository):
        self.repo = repository
        self.service = StoryService()

    def execute(self, dto: CreateStoryDTO) -> dict:
        """Создает историю и генерирует QR-код"""
        story = self.service.create_story(
            title=dto.title,
            content=dto.content,
            location=dto.location,
            author_id=dto.author_id
        )

        saved_story = self.repo.save(story)
        return {
            "id": saved_story.id,
            "qr_url": saved_story.qr_code.url
        }
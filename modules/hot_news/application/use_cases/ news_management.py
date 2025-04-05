from ..domain.entities import NewsItem
from ..domain.services import NewsValidator
from .dto.news_dto import CreateNewsDTO


class CreateNewsUseCase:
    def __init__(self, news_repository, news_validator: NewsValidator):
        self.repo = news_repository
        self.validator = news_validator

    def execute(self, dto: CreateNewsDTO) -> NewsItem:
        """Создает новую новостную запись"""
        self.validator.validate_news(dto.to_dict())

        news_item = NewsItem(
            id=None,
            title=dto.title,
            content=dto.content,
            category=dto.category,
            priority=self.validator.determine_priority(dto.to_dict()),
            publish_date=datetime.now(),
            source=dto.source,
            location=dto.location,
            related_links=dto.related_links,
            image_url=dto.image_url
        )

        return self.repo.save(news_item)
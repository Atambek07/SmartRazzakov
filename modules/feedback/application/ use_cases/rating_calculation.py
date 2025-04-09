# modules/feedback/application/use_cases/rating_calculation.py
from abc import ABC, abstractmethod
from ...domain.entities import RatingSummary
from ...application.dto import RatingSummaryDTO, ContentRefDTO
from core.utils import BaseUseCase
from core.integrations import AnalyticsService

class RatingRepository(ABC):
    @abstractmethod
    def get_ratings(self, content_ref: ContentRefDTO) -> RatingSummary:
        pass

class CalculateRatingUseCase(BaseUseCase):
    def __init__(self, repo: RatingRepository, analytics: AnalyticsService):
        self.repo = repo
        self.analytics = analytics

    def execute(self, content_ref: ContentRefDTO) -> RatingSummaryDTO:
        summary = self.repo.get_ratings(content_ref)
        
        # Анализ данных
        analytics_data = self.analytics.analyze_ratings(
            content_ref=content_ref,
            raw_data=summary.rating_distribution
        )
        
        return RatingSummaryDTO(
            total_reviews=summary.total_reviews,
            average_rating=summary.average_rating,
            rating_distribution=summary.rating_distribution,
            compared_to_similar=analytics_data.get('percentile')
        )

class RatingUpdateCoordinator:
    def __init__(self, rating_repo, module_service_resolver):
        self.rating_repo = rating_repo
        self.service_resolver = module_service_resolver

    def update_content_rating(self, content_type: str, object_id: int, module: str):
        # Получаем сервис целевого модуля
        service = self.service_resolver.resolve(module)
        
        # Рассчитываем новый рейтинг
        summary = self.rating_repo.get_ratings(
            ContentRefDTO(
                content_type=content_type,
                object_id=object_id,
                module=module
            )
        )
        
        # Обновляем в целевом модуле
        service.update_rating(object_id, summary.average_rating)
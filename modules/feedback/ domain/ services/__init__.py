# modules/feedback/domain/services/__init__.py
"""
Интерфейсы доменных сервисов для работы с отзывами и рейтингами
"""

from abc import ABC, abstractmethod
from ...domain.entities import ReviewEntity, RatingSummary

class BaseRatingService(ABC):
    @abstractmethod
    def calculate_rating(self, reviews: list[ReviewEntity]) -> RatingSummary:
        pass

class BaseReviewService(ABC):
    @abstractmethod
    def validate_review_content(self, review: ReviewEntity) -> bool:
        pass

class BaseSentimentAnalyzer(ABC):
    @abstractmethod
    def analyze(self, text: str) -> dict:
        pass

__all__ = ['BaseRatingService', 'BaseReviewService', 'BaseSentimentAnalyzer']
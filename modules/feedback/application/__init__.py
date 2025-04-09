# modules/feedback/application/__init__.py
"""
Главный экспортной интерфейс Application Layer модуля Feedback

Предоставляет:
- Все DTO для работы с отзывами и рейтингами
- Основные Use Cases
- Сервисы для интеграции
"""

from .dto import (
    ReviewCreateDTO,
    ReviewUpdateDTO,
    ReviewResponseDTO,
    RatingCreateDTO,
    RatingSummaryDTO,
    ContentRefDTO
)

from .use_cases import (
    CreateReviewUseCase,
    UpdateReviewUseCase,
    GetReviewUseCase,
    CalculateRatingUseCase,
    ModerateReviewUseCase,
    GenerateSummaryReportUseCase
)

# Экспорт интерфейсов для внедрения зависимостей
__all__ = [
    # DTO
    'ReviewCreateDTO',
    'ReviewUpdateDTO',
    'ReviewResponseDTO',
    'RatingCreateDTO',
    'RatingSummaryDTO',
    'ContentRefDTO',
    
    # Use Cases
    'CreateReviewUseCase',
    'UpdateReviewUseCase',
    'GetReviewUseCase',
    'CalculateRatingUseCase',
    'ModerateReviewUseCase',
    'GenerateSummaryReportUseCase',
    
    # Interfaces
    'ReviewRepository',
    'RatingRepository',
    'ModerationRepository'
]

# Импорт интерфейсов после объявления __all__ для избежания циклических импортов
from .use_cases.review_management import ReviewRepository
from .use_cases.rating_calculation import RatingRepository
from .use_cases.feedback_moderation import ModerationRepository
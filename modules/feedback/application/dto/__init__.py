# modules/feedback/application/dto/__init__.py
"""
DTO модуля Feedback для безопасной передачи данных между слоями
"""
from .review_dto import *
from .rating_dto import *

__all__ = [
    'ReviewCreateDTO',
    'ReviewUpdateDTO',
    'ReviewResponseDTO',
    'RatingCreateDTO',
    'RatingSummaryDTO',
    'ContentRefDTO'
]
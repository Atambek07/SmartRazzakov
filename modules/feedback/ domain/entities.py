# modules/feedback/domain/entities.py
from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List, Dict

@dataclass
class ReviewEntity:
    id: Optional[int]
    author_id: int
    content_type: str
    object_id: int
    rating: int
    text: Optional[str]
    media: Dict[str, List[str]]  # {'audio': [], 'video': [], 'images': []}
    tags: List[str]
    status: str  # 'pending', 'approved', 'rejected'
    created_at: datetime
    updated_at: datetime
    source_module: str
    helpful_count: int = 0
    reply_count: int = 0

    def validate(self):
        """Базовые проверки целостности данных"""
        if self.rating < 1 or self.rating > 5:
            raise ValueError("Rating must be between 1 and 5")
        
        if not self.text and not self.media:
            raise ValueError("Review must have text or media content")

@dataclass
class RatingSummary:
    content_type: str
    object_id: int
    average_rating: float
    total_reviews: int
    rating_distribution: Dict[int, int]  # {1: count, 2: count, ...}
    calculated_at: datetime
    confidence_score: Optional[float] = None
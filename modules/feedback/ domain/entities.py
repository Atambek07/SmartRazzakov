from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Optional

class FeedbackType(Enum):
    SERVICE = "service"
    PRODUCT = "product"
    GOVERNMENT = "government"
    TRANSPORT = "transport"

class ReviewStatus(Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"

@dataclass
class Review:
    id: str
    author_id: str
    target_id: str  # ID объекта отзыва (бизнес, служба и т.д.)
    feedback_type: FeedbackType
    text: str
    rating: int  # 1-5
    status: ReviewStatus
    created_at: datetime
    modified_at: Optional[datetime] = None
    photos: Optional[list[str]] = None
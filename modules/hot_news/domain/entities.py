from datetime import datetime
from enum import Enum
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, validator
from uuid import UUID, uuid4

class NewsCategory(str, Enum):
    TRANSPORT = "transport"
    EDUCATION = "education"
    CULTURE = "culture"
    EMERGENCY = "emergency"
    GOVERNMENT = "government"
    COMMUNITY = "community"
    ECONOMY = "economy"
    HEALTH = "health"
    OTHER = "other"

class NewsPriority(int, Enum):
    LOW = 1
    NORMAL = 2
    HIGH = 3
    CRITICAL = 4

class NewsArticle(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    title: str = Field(..., min_length=5, max_length=200)
    content: str = Field(..., min_length=50)
    category: NewsCategory
    priority: NewsPriority = NewsPriority.NORMAL
    geo_location: Optional[str] = None
    sources: List[str] = Field(default_factory=list)
    media_attachments: List[str] = Field(default_factory=list)
    sentiment_score: float = Field(0.0, ge=-1.0, le=1.0)
    views_count: int = 0
    is_published: bool = False
    author_id: UUID
    created_at: datetime = Field(default_factory=datetime.now)
    modified_at: datetime = Field(default_factory=datetime.now)
    publish_at: Optional[datetime] = None

    @validator('sources')
    def validate_sources(cls, v):
        if not all(source.startswith(('http://', 'https://', '/')) for source in v):
            raise ValueError('Invalid source format')
        return v

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat(),
            UUID: lambda v: str(v)
        }

class NewsSubscription(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    user_id: UUID
    categories: List[NewsCategory] = Field(..., min_items=1)
    notification_channels: Dict[str, bool] = Field(
        default_factory=lambda: {
            'email': False,
            'push': True,
            'sms': False
        }
    )
    preferred_language: str = 'ru'
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.now)

    @validator('preferred_language')
    def validate_language(cls, v):
        if v not in ['ru', 'ky', 'en']:
            raise ValueError('Unsupported language')
        return v

class EmergencyAlert(NewsArticle):
    protocol_triggers: Dict[str, Any] = Field(default_factory=dict)
    affected_areas: List[str] = Field(...)
    expiration_time: datetime

    @validator('category')
    def validate_category(cls, v):
        if v != NewsCategory.EMERGENCY:
            raise ValueError('Emergency alert must have EMERGENCY category')
        return v
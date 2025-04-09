from datetime import datetime
from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, validator
from modules.hot_news.domain.entities import NewsCategory, NewsPriority

class NewsCreateDTO(BaseModel):
    title: str
    content: str
    category: NewsCategory
    priority: NewsPriority = NewsPriority.NORMAL
    geo_location: Optional[str] = None
    sources: List[str]  # Ссылки на исходные данные (GovConnect, CommunityHub и т.д.)
    media_attachments: List[str] = []
    publish_at: Optional[datetime] = None

    @validator('title')
    def title_not_empty(cls, v):
        if not v.strip():
            raise ValueError('Title cannot be empty')
        return v.strip()

    @validator('content')
    def content_length(cls, v):
        if len(v) < 50:
            raise ValueError('Content too short (min 50 chars)')
        return v

    class Config:
        use_enum_values = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class NewsUpdateDTO(NewsCreateDTO):
    title: Optional[str] = None
    content: Optional[str] = None
    category: Optional[NewsCategory] = None
    priority: Optional[NewsPriority] = None

class NewsResponseDTO(NewsCreateDTO):
    id: str
    created_at: datetime
    modified_at: datetime
    views_count: int = 0
    is_published: bool = False
    author_id: Optional[str] = None

    class Config:
        orm_mode = True
from typing import List, Optional
from pydantic import BaseModel, validator
from modules.hot_news.domain.entities import NewsCategory

class SubscriptionCreateDTO(BaseModel):
    user_id: str
    categories: List[NewsCategory]
    notify_by_email: bool = False
    notify_by_push: bool = True
    notify_by_sms: bool = False
    preferred_language: str = "ru"

    @validator('categories')
    def validate_categories(cls, v):
        if not v:
            raise ValueError('At least one category required')
        return v

    @validator('preferred_language')
    def validate_language(cls, v):
        if v not in ["ru", "ky", "en"]:
            raise ValueError('Unsupported language')
        return v

class SubscriptionUpdateDTO(SubscriptionCreateDTO):
    categories: Optional[List[NewsCategory]] = None
    notify_by_email: Optional[bool] = None
    notify_by_push: Optional[bool] = None
    notify_by_sms: Optional[bool] = None
    preferred_language: Optional[str] = None

class SubscriptionResponseDTO(SubscriptionCreateDTO):
    id: str
    created_at: datetime
    is_active: bool = True

    class Config:
        orm_mode = True
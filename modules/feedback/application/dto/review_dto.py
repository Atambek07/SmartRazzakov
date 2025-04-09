# modules/feedback/application/dto/review_dto.py
from pydantic import BaseModel, Field, validator
from typing import Optional, List, Dict
from datetime import datetime
from enum import Enum

class ReviewType(str, Enum):
    BUSINESS = 'business'
    SERVICE = 'service'
    GOVERNMENT = 'government'
    EDUCATIONAL = 'educational'
    MEDICAL = 'medical'

class ReviewMediaDTO(BaseModel):
    audio_url: Optional[str] = Field(
        None, 
        example="/media/reviews/audio/sample.mp3",
        description="URL аудиозаписи отзыва"
    )
    video_url: Optional[str] = Field(
        None,
        example="/media/reviews/video/sample.mp4",
        description="URL видеоотзыва"
    )
    images: List[str] = Field(
        default_factory=list,
        example=["/media/reviews/images/img1.jpg"],
        description="Список URL изображений"
    )

class ReviewCreateDTO(BaseModel):
    content_type: ReviewType = Field(
        ..., 
        example="business",
        description="Тип оцениваемого объекта"
    )
    object_id: int = Field(
        ..., 
        example=123,
        description="ID объекта в исходной системе"
    )
    rating: int = Field(
        ..., 
        ge=1, 
        le=5,
        example=5,
        description="Оценка от 1 до 5 звезд"
    )
    text: Optional[str] = Field(
        None,
        min_length=10,
        max_length=2000,
        example="Отличный сервис! Рекомендую всем.",
        description="Текст отзыва"
    )
    media: ReviewMediaDTO = Field(
        default_factory=ReviewMediaDTO,
        description="Медиа-вложения отзыва"
    )
    tags: List[str] = Field(
        default_factory=list,
        example=["#семейный_отдых", "#бюджетно"],
        max_items=5,
        description="Теги для категоризации отзыва"
    )
    source_module: str = Field(
        ..., 
        example="edu_space",
        description="Исходный модуль системы"
    )

    @validator('tags')
    def validate_tags(cls, v):
        if any(len(tag) > 50 for tag in v):
            raise ValueError("Максимальная длина тега 50 символов")
        return v

class ReviewUpdateDTO(ReviewCreateDTO):
    status: Optional[str] = Field(
        None,
        example="approved",
        description="Статус модерации"
    )

class ReviewResponseDTO(ReviewCreateDTO):
    id: int
    author_id: int
    created_at: datetime
    updated_at: datetime
    status: str
    moderation_comment: Optional[str]
    helpful_count: int = 0
    reply_count: int = 0

    class Config:
        orm_mode = True
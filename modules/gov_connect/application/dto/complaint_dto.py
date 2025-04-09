# modules/gov_connect/application/dto/complaint_dto.py
from datetime import datetime
from pydantic import BaseModel, Field, validator, HttpUrl
from typing import Optional, List, Literal
from uuid import UUID
from core.models.base import Point

class ComplaintBaseDTO(BaseModel):
    title: str = Field(
        ...,
        min_length=5,
        max_length=120,
        example="Яма на проспекте Абая",
        description="Краткое описание проблемы"
    )
    description: str = Field(
        ...,
        min_length=20,
        max_length=2000,
        example="Глубокая яма размером 1x1м перед домом №15",
        description="Подробное описание проблемы"
    )
    location: Point = Field(
        ...,
        example={"type": "Point", "coordinates": [76.915982, 43.238293]},
        description="Геокоординаты проблемы в формате GeoJSON"
    )
    category: Literal[
        'roads', 
        'lighting', 
        'utilities', 
        'sanitation', 
        'public_transport',
        'parks',
        'other'
    ] = Field(
        ...,
        example="roads",
        description="Категория проблемы"
    )
    photo_urls: List[HttpUrl] = Field(
        ...,
        min_items=1,
        max_items=5,
        example=["https://storage.example.com/photo1.jpg"],
        description="Ссылки на фотографии проблемы"
    )
    audio_url: Optional[HttpUrl] = Field(
        None,
        example="https://storage.example.com/audio.mp3",
        description="Ссылка на аудиозапись (для голосовых жалоб)"
    )

    @validator('photo_urls')
    def validate_photo_urls(cls, v):
        if not all(url.startswith('https://') for url in v):
            raise ValueError('Фото должны быть загружены через HTTPS')
        return v

class ComplaintCreateDTO(ComplaintBaseDTO):
    user_id: UUID = Field(
        ...,
        example="3fa85f64-5717-4562-b3fc-2c963f66afa6",
        description="ID пользователя"
    )
    anonymous: bool = Field(
        False,
        description="Анонимная жалоба"
    )

class ComplaintUpdateDTO(BaseModel):
    status: Optional[Literal['new', 'in_progress', 'resolved', 'rejected']] = None
    municipal_comment: Optional[str] = Field(
        None,
        max_length=500,
        example="Ремонт запланирован на 15.09.2023",
        description="Комментарий муниципальной службы"
    )
    before_photo_url: Optional[HttpUrl] = Field(
        None,
        description="Фото до решения проблемы"
    )
    after_photo_url: Optional[HttpUrl] = Field(
        None,
        description="Фото после решения проблемы"
    )

class ComplaintResponseDTO(ComplaintBaseDTO):
    id: UUID = Field(..., description="Уникальный идентификатор жалобы")
    created_at: datetime = Field(..., example="2023-08-20T12:34:56Z")
    updated_at: datetime = Field(..., example="2023-08-21T09:45:23Z")
    status: str = Field(..., example="in_progress")
    tracking_code: str = Field(
        ...,
        example="GOV-5XQ9-7B2F",
        description="Публичный код для отслеживания"
    )
    municipal_comment: Optional[str] = None
    before_photo_url: Optional[HttpUrl] = None
    after_photo_url: Optional[HttpUrl] = None
    votes_count: int = Field(
        0,
        description="Количество голосов поддержки от других пользователей"
    )
    similar_complaints: List[UUID] = Field(
        default_factory=list,
        description="ID похожих жалоб"
    )

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class ComplaintStatusDTO(BaseModel):
    status: Literal['new', 'in_progress', 'resolved', 'rejected']
    public_comment: Optional[str] = Field(
        None,
        max_length=1000,
        description="Публичный комментарий для граждан"
    )
    internal_comment: Optional[str] = Field(
        None,
        max_length=1000,
        description="Внутренний комментарий для сотрудников"
    )
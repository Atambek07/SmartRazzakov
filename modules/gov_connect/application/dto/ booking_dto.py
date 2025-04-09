# modules/gov_connect/application/dto/booking_dto.py
from datetime import datetime, time
from pydantic import BaseModel, Field, validator
from typing import Optional, List
from uuid import UUID

class SlotAvailabilityDTO(BaseModel):
    start_time: datetime = Field(
        ...,
        example="2023-09-15T09:00:00Z",
        description="Начало временного слота"
    )
    end_time: datetime = Field(
        ...,
        example="2023-09-15T09:30:00Z",
        description="Конец временного слота"
    )
    capacity: int = Field(
        ...,
        ge=1,
        le=50,
        example=10,
        description="Количество доступных мест"
    )

    @validator('end_time')
    def validate_time_range(cls, v, values):
        if 'start_time' in values and v <= values['start_time']:
            raise ValueError('End time must be after start time')
        return v

class BookingBaseDTO(BaseModel):
    service_type: str = Field(
        ...,
        example="passport_renewal",
        description="Тип государственной услуги"
    )
    office_id: UUID = Field(
        ...,
        example="550e8400-e29b-41d4-a716-446655440000",
        description="ID офиса предоставления услуги"
    )
    preferred_time: Optional[List[datetime]] = Field(
        None,
        description="Предпочитаемое время визита"
    )

class BookingCreateDTO(BookingBaseDTO):
    user_id: UUID = Field(
        ...,
        description="ID пользователя"
    )
    complaint_id: Optional[UUID] = Field(
        None,
        description="ID связанной жалобы (если применимо)"
    )
    documents: List[str] = Field(
        ...,
        min_items=1,
        example=["identity_document"],
        description="Список необходимых документов"
    )

class BookingUpdateDTO(BaseModel):
    status: Optional[Literal['pending', 'confirmed', 'canceled', 'completed']] = None
    actual_time: Optional[datetime] = Field(
        None,
        description="Фактическое время визита"
    )
    notes: Optional[str] = Field(
        None,
        max_length=500,
        description="Дополнительные заметки"
    )

class BookingResponseDTO(BookingBaseDTO):
    id: UUID = Field(..., description="Уникальный идентификатор записи")
    created_at: datetime = Field(..., example="2023-08-20T12:34:56Z")
    status: str = Field(..., example="confirmed")
    qr_code_url: Optional[str] = Field(
        None,
        example="https://storage.example.com/qr.png",
        description="Ссылка на QR-код для посещения"
    )
    queue_position: Optional[int] = Field(
        None,
        ge=1,
        description="Позиция в очереди"
    )
    estimated_wait_time: Optional[int] = Field(
        None,
        ge=0,
        description="Примерное время ожидания в минутах"
    )
    confirmation_code: Optional[str] = Field(
        None,
        example="5XQ9-7B2F",
        description="Код подтверждения для SMS"
    )

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
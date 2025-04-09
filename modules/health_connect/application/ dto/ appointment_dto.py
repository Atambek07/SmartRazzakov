# modules/health_connect/application/dto/appointment_dto.py
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, validator
from ...domain.entities import AppointmentStatus

class AppointmentBase(BaseModel):
    patient_id: str = Field(..., description="ID пациента")
    provider_id: str = Field(..., description="ID медицинского специалиста")
    scheduled_time: datetime = Field(..., description="Запланированное время приёма")
    reason: Optional[str] = Field(None, max_length=500, description="Причина визита")
    notes: Optional[str] = Field(None, max_length=1000, description="Дополнительные заметки")

    @validator('scheduled_time')
    def validate_scheduled_time(cls, v):
        if v <= datetime.now():
            raise ValueError("Appointment time must be in the future")
        return v

class AppointmentCreate(AppointmentBase):
    pass

class AppointmentUpdate(BaseModel):
    scheduled_time: Optional[datetime] = None
    status: Optional[AppointmentStatus] = None
    reason: Optional[str] = None
    notes: Optional[str] = None

    @validator('scheduled_time')
    def validate_updated_time(cls, v):
        if v and v <= datetime.now():
            raise ValueError("Updated appointment time must be in the future")
        return v

class AppointmentResponse(AppointmentBase):
    id: str = Field(..., description="Уникальный идентификатор записи")
    status: AppointmentStatus = Field(..., description="Текущий статус записи")
    created_at: datetime = Field(..., description="Время создания записи")
    modified_at: Optional[datetime] = Field(None, description="Время последнего изменения")

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class AppointmentSearch(BaseModel):
    patient_id: Optional[str] = None
    provider_id: Optional[str] = None
    status: Optional[AppointmentStatus] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    facility_id: Optional[str] = None
    specialization: Optional[str] = None

    @validator('end_date')
    def validate_date_range(cls, v, values):
        if v and values.get('start_date') and v < values['start_date']:
            raise ValueError("End date must be after start date")
        return v
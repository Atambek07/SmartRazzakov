# modules/health_connect/application/dto/medical_dto.py
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, validator
from ...domain.entities import MedicalRecordType

class MedicalRecordBase(BaseModel):
    patient_id: str = Field(..., description="ID пациента")
    record_type: MedicalRecordType = Field(..., description="Тип медицинской записи")
    title: str = Field(..., max_length=200, description="Краткое описание записи")
    description: str = Field(..., max_length=2000, description="Подробное описание")
    date: datetime = Field(..., description="Дата возникновения/обнаружения")
    provider_id: Optional[str] = Field(None, description="ID связанного специалиста")
    attachments: List[str] = Field(default_factory=list, description="Ссылки на вложения")
    is_confidential: bool = Field(False, description="Флаг конфиденциальности записи")

    @validator('date')
    def validate_record_date(cls, v):
        if v > datetime.now():
            raise ValueError("Record date cannot be in the future")
        return v

class MedicalRecordCreate(MedicalRecordBase):
    pass

class MedicalRecordUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    record_type: Optional[MedicalRecordType] = None
    is_confidential: Optional[bool] = None
    attachments: Optional[List[str]] = None

class MedicalRecordResponse(MedicalRecordBase):
    id: str = Field(..., description="Уникальный идентификатор записи")
    created_at: datetime = Field(..., description="Время создания записи в системе")
    modified_at: Optional[datetime] = Field(None, description="Время последнего изменения")

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class MedicalRecordSearch(BaseModel):
    patient_id: str
    record_type: Optional[MedicalRecordType] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    provider_id: Optional[str] = None
    keywords: Optional[str] = None

    @validator('end_date')
    def validate_date_range(cls, v, values):
        if v and values.get('start_date') and v < values['start_date']:
            raise ValueError("End date must be after start date")
        return v
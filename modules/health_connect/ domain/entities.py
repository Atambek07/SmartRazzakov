# modules/health_connect/domain/entities.py
from datetime import datetime
from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field
from uuid import UUID

class MedicalRecordType(str, Enum):
    ALLERGY = "allergy"
    DIAGNOSIS = "diagnosis"
    PRESCRIPTION = "prescription"
    VACCINATION = "vaccination"
    PROCEDURE = "procedure"
    LAB_RESULT = "lab_result"
    IMAGING = "imaging"
    NOTE = "clinical_note"

class AppointmentStatus(str, Enum):
    REQUESTED = "requested"
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    RESCHEDULED = "rescheduled"

class MedicalRecord(BaseModel):
    id: UUID = Field(..., description="Уникальный идентификатор записи")
    patient_id: UUID = Field(..., description="Идентификатор пациента")
    record_type: MedicalRecordType = Field(..., description="Тип медицинской записи")
    title: str = Field(..., max_length=200, description="Заголовок записи")
    content: dict = Field(..., description="Структурированное содержимое записи")
    created_at: datetime = Field(default_factory=datetime.now, description="Дата создания")
    updated_at: Optional[datetime] = Field(None, description="Дата последнего обновления")
    provider_id: Optional[UUID] = Field(None, description="Ответственный врач")
    is_confidential: bool = Field(False, description="Конфиденциальность записи")
    related_appointment: Optional[UUID] = Field(None, description="Связанная запись")

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat(),
            UUID: lambda v: str(v)
        }

class Appointment(BaseModel):
    id: UUID = Field(..., description="Уникальный идентификатор записи")
    patient_id: UUID = Field(..., description="Идентификатор пациента")
    provider_id: UUID = Field(..., description="Идентификатор врача")
    scheduled_time: datetime = Field(..., description="Запланированное время")
    status: AppointmentStatus = Field(AppointmentStatus.REQUESTED, description="Статус записи")
    duration: int = Field(30, ge=15, le=120, description="Длительность приема (мин)")
    reason: Optional[str] = Field(None, max_length=500, description="Причина визита")
    created_at: datetime = Field(default_factory=datetime.now, description="Дата создания")
    updated_at: Optional[datetime] = Field(None, description="Дата обновления")
    video_link: Optional[str] = Field(None, description="Ссылка на телемедицинскую сессию")

    def is_active(self) -> bool:
        return self.status in {
            AppointmentStatus.REQUESTED,
            AppointmentStatus.CONFIRMED,
            AppointmentStatus.IN_PROGRESS
        }

class HealthcareProvider(BaseModel):
    id: UUID = Field(..., description="Уникальный идентификатор врача")
    user_id: UUID = Field(..., description="Связанный аккаунт пользователя")
    specializations: List[str] = Field(..., description="Специализации")
    license_number: str = Field(..., min_length=8, description="Номер лицензии")
    facilities: List[UUID] = Field(..., description="Прикрепленные медучреждения")
    available_hours: dict = Field(
        default_factory=lambda: {
            "mon": ["09:00-17:00"],
            "tue": ["09:00-17:00"],
            "wed": ["09:00-17:00"],
            "thu": ["09:00-17:00"],
            "fri": ["09:00-17:00"]
        },
        description="Расписание работы"
    )
    is_verified: bool = Field(False, description="Верифицирован ли врач")
    languages: List[str] = Field(["ru"], description="Языки общения")
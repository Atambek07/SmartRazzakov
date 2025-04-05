from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import List, Optional

class BloodType(Enum):
    O_POSITIVE = "O+"
    A_POSITIVE = "A+"
    B_NEGATIVE = "B-"
    # ... другие типы

class AppointmentStatus(Enum):
    SCHEDULED = "scheduled"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

@dataclass
class MedicalRecord:
    id: str
    patient_id: str
    diagnosis: str
    treatment: str
    doctor_id: str
    date: datetime
    attachments: List[str]  # Ссылки на файлы
    is_emergency: bool = False
    notes: Optional[str] = None

@dataclass
class Appointment:
    id: str
    patient_id: str
    doctor_id: str
    datetime: datetime
    duration: int  # минуты
    status: AppointmentStatus
    video_link: Optional[str] = None
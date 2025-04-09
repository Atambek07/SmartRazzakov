# modules/gov_connect/domain/entities.py
"""
Ядро бизнес-логики модуля GovConnect

Содержит:
- Базовые классы Value Objects
- Агрегаты
- Корневые сущности
"""

from datetime import datetime
from enum import Enum
from typing import Optional, List, Dict
from uuid import UUID, uuid4
from pydantic import BaseModel, Field
from core.models.geo import Point

from pydantic import BaseModel
from typing import List, Optional
from uuid import UUID, uuid4
from datetime import datetime
from enum import Enum

class ComplaintStatus(str, Enum):
    NEW = 'new'
    IN_PROGRESS = 'in_progress'
    RESOLVED = 'resolved'
    REJECTED = 'rejected'

class BookingStatus(str, Enum):
    PENDING = 'pending'
    CONFIRMED = 'confirmed'
    CANCELED = 'canceled'
    COMPLETED = 'completed'

class VotingStatus(str, Enum):
    DRAFT = 'draft'
    ACTIVE = 'active'
    COMPLETED = 'completed'

class Complaint(BaseModel):
    """Агрегат для управления жизненным циклом жалобы"""
    id: UUID = Field(default_factory=uuid4)
    user_id: UUID
    title: str
    description: str
    location: Point
    category: str
    status: ComplaintStatus = ComplaintStatus.NEW
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    photo_urls: List[str] = []
    audio_url: Optional[str] = None
    related_complaints: List[UUID] = []
    votes: Dict[str, int] = Field(default_factory=dict)

    def change_status(self, new_status: ComplaintStatus):
        allowed_transitions = {
            ComplaintStatus.NEW: [ComplaintStatus.IN_PROGRESS, ComplaintStatus.REJECTED],
            ComplaintStatus.IN_PROGRESS: [ComplaintStatus.RESOLVED, ComplaintStatus.REJECTED],
            ComplaintStatus.REJECTED: [],
            ComplaintStatus.RESOLVED: []
        }
        if new_status not in allowed_transitions[self.status]:
            raise ValueError(f"Invalid status transition from {self.status} to {new_status}")
        self.status = new_status
        self.updated_at = datetime.utcnow()

class Booking(BaseModel):
    """Сущность для управления записями в госучреждения"""
    id: UUID = Field(default_factory=uuid4)
    user_id: UUID
    service_type: str
    office_id: UUID
    scheduled_time: datetime
    status: BookingStatus = BookingStatus.PENDING
    qr_code_url: Optional[str] = None
    documents: List[str] = []
    confirmation_code: Optional[str] = None

class Voting(BaseModel):
    """Агрегат для управления голосованиями"""
    id: UUID = Field(default_factory=uuid4)
    title: str
    description: str
    options: List[str]
    start_date: datetime
    end_date: datetime
    min_age: int = 18
    residency_required: bool = True
    votes: Dict[str, int] = Field(default_factory=dict)

    def is_active(self):
        now = datetime.utcnow()
        return self.start_date <= now <= self.end_date

class Document(BaseModel):
    """Value Object для управления документами"""
    id: UUID = Field(default_factory=uuid4)
    user_id: UUID
    complaint_id: Optional[UUID] = None
    file_url: str
    uploaded_at: datetime = Field(default_factory=datetime.utcnow)
    
    
class EmergencyAlertType(str, Enum):
    DISASTER = "natural_disaster"
    ACCIDENT = "major_accident"
    SECURITY = "security_threat"
    TEST = "test_alert"

class EmergencyAlert(BaseModel):
    id: UUID = uuid4()
    message: str
    alert_type: EmergencyAlertType
    zones: List[str]  # Гео-JSON полигоны
    channels: List[str]  # sms, email, sirens, mobile_push
    created_at: datetime = datetime.utcnow()
    status: str = "pending"

class EmergencyZone(BaseModel):
    id: UUID = uuid4()
    name: str
    geojson: dict  # Геометрия зоны
    population: int
    priority: int
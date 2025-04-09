# modules/edu_space/application/dto/classroom_dto.py
from pydantic import BaseModel, Field, validator
from datetime import datetime
from uuid import UUID
from typing import Optional, List
from enum import Enum

class CourseLevel(str, Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"

class CourseCreateRequest(BaseModel):
    title: str = Field(..., min_length=5, max_length=100)
    tutor_id: UUID
    subject: str
    schedule: dict = Field(
        ..., 
        example={
            "days": ["Monday", "Wednesday"],
            "time": "15:00-17:00",
            "timezone": "Asia/Almaty"
        }
    )
    price: float = Field(ge=0, description="Price in KZT")
    level: CourseLevel
    capacity: int = Field(20, ge=1, le=50)
    prerequisites: List[str] = Field(default_factory=list)

    @validator('schedule')
    def validate_schedule(cls, v):
        required_keys = {'days', 'time', 'timezone'}
        if not all(key in v for key in required_keys):
            raise ValueError('Invalid schedule format')
        return v

class CourseResponse(BaseModel):
    id: UUID
    title: str
    tutor_name: str
    schedule: dict
    enrolled_students: int
    available_seats: int
    rating: float
    price_display: str

class EnrollmentRequest(BaseModel):
    course_id: UUID
    student_id: UUID
    payment_method_token: Optional[str] = None
    parent_consent_code: Optional[str] = None

class LiveSessionDetails(BaseModel):
    start_time: datetime
    duration: int = Field(..., ge=30, le=180)
    materials: List[str] = []
    recording_url: Optional[str] = None
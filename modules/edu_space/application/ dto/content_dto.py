# modules/edu_space/application/dto/content_dto.py
from pydantic import BaseModel, HttpUrl, Field
from uuid import UUID
from enum import Enum
from typing import Optional, List
from datetime import datetime

class ContentType(str, Enum):
    LESSON = "lesson"
    TEST = "test"
    VIDEO = "video"
    EBOOK = "ebook"
    INTERACTIVE = "interactive"

class ContentUploadRequest(BaseModel):
    title: str = Field(..., max_length=200)
    content_type: ContentType
    subject: str
    grade_level: int = Field(..., ge=1, le=11)
    file_url: HttpUrl
    author_id: UUID
    interactive_config: Optional[dict] = Field(
        None,
        description="JSON configuration for interactive elements"
    )

class ContentResponse(BaseModel):
    id: UUID
    title: str
    type: ContentType
    preview_url: HttpUrl
    author_name: str
    rating: float
    difficulty: str
    interactive_available: bool
    created_at: datetime

class ContentSearchRequest(BaseModel):
    query: Optional[str] = None
    subjects: Optional[List[str]] = None
    types: Optional[List[ContentType]] = None
    grade_level: Optional[int] = None
    min_rating: float = 4.0
    max_duration: Optional[int] = None

class TestSubmission(BaseModel):
    user_id: UUID
    content_id: UUID
    answers: dict
    session_id: UUID
    start_time: datetime
    end_time: datetime
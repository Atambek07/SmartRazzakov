from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import List

class ContentType(Enum):
    VIDEO = "video"
    PDF = "pdf"
    QUIZ = "quiz"
    INTERACTIVE = "interactive"

class DifficultyLevel(Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"

@dataclass
class EducationalContent:
    id: str
    title: str
    content_type: ContentType
    difficulty: DifficultyLevel
    subject: str
    author_id: str
    created_at: datetime
    metadata: dict  # duration, file_size, etc.

@dataclass
class VirtualClassroom:
    id: str
    teacher_id: str
    student_ids: List[str]
    content_ids: List[str]
    schedule: dict  # {start_time, end_time, recurrence}
    status: str  # planned, ongoing, completed
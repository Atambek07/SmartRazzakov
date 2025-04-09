from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import List, Dict, Optional
from uuid import UUID

class UserRole(str, Enum):
    STUDENT = "student"
    TEACHER = "teacher"
    TUTOR = "tutor"
    PARENT = "parent"
    ADMIN = "admin"

class ContentType(str, Enum):
    LESSON = "lesson"
    TEST = "test"
    VIDEO = "video"
    EBOOK = "ebook"
    AUDIOBOOK = "audiobook"
    INTERACTIVE = "interactive"
    GAME = "game"

class CourseLevel(str, Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"

@dataclass(frozen=True)
class UserProfile:
    id: UUID
    role: UserRole
    first_name: str
    last_name: str
    email: str
    grade_level: Optional[int] = None
    subjects: List[str] = field(default_factory=list)
    achievements: List[str] = field(default_factory=list)

@dataclass
class EducationalContent:
    id: UUID
    title: str
    content_type: ContentType
    subject: str
    grade_level: int
    author_id: UUID
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    file_url: str
    metadata: Dict[str, any] = field(default_factory=dict)
    is_published: bool = False

    def publish(self) -> None:
        if not self.file_url:
            raise ValueError("Cannot publish content without file URL")
        self.is_published = True
        self.updated_at = datetime.now()

@dataclass
class Course:
    id: UUID
    title: str
    tutor_id: UUID
    schedule: Dict[str, str]
    price: float
    level: CourseLevel
    capacity: int = 30
    enrolled_students: List[UUID] = field(default_factory=list)
    rating: float = 0.0

    def enroll_student(self, student_id: UUID) -> None:
        if student_id in self.enrolled_students:
            raise ValueError("Student already enrolled")
        if len(self.enrolled_students) >= self.capacity:
            raise ValueError("Course capacity exceeded")
        self.enrolled_students.append(student_id)

@dataclass(frozen=True)
class School:
    id: UUID
    name: str
    address: str
    rating: float
    available_seats: Dict[int, int]  # grade: available_seats
    programs: List[str]
    photos: List[str]

@dataclass(frozen=True)
class LearningProgress:
    user_id: UUID
    content_id: UUID
    score: float
    completion_date: datetime
    attempts: int = 1
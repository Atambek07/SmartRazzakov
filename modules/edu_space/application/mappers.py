from uuid import UUID
from datetime import datetime
from typing import Any, Dict
from ...domain.entities import (
    EducationalContent,
    Course,
    UserProfile,
    LearningProgress
)
from .dto import (
    CourseCreateRequest,
    CourseResponse,
    ContentUploadRequest,
    ContentResponse,
    TutorProfileResponse
)

class EduSpaceMapper:
    """Преобразует объекты между слоями приложения и домена"""

    @staticmethod
    def map_course_create_request_to_entity(
        request: CourseCreateRequest,
        tutor_id: UUID
    ) -> Dict[str, Any]:
        """Преобразует DTO запроса в данные для создания курса"""
        return {
            'title': request.title,
            'tutor_id': tutor_id,
            'schedule': request.schedule,
            'price': request.price,
            'level': request.level,
            'capacity': request.capacity,
            'metadata': {
                'prerequisites': request.prerequisites,
                'subject': request.subject
            }
        }

    @staticmethod
    def map_course_to_response(
        course: Course,
        tutor_name: str,
        enrolled_count: int
    ) -> CourseResponse:
        """Преобразует доменную модель курса в DTO ответа"""
        return CourseResponse(
            id=course.id,
            title=course.title,
            tutor_name=tutor_name,
            schedule=course.schedule,
            enrolled_students=enrolled_count,
            available_seats=course.capacity - enrolled_count,
            rating=course.rating,
            price_display=f"{course.price} {course.currency}",
            level=course.level.value
        )

    @staticmethod
    def map_content_upload_request_to_entity(
        request: ContentUploadRequest,
        author_id: UUID
    ) -> EducationalContent:
        """Создает доменную модель контента из DTO запроса"""
        return EducationalContent(
            id=UUID(int=0),  # Генерируется репозиторием
            title=request.title,
            content_type=request.content_type,
            subject=request.subject,
            grade_level=request.grade_level,
            author_id=author_id,
            file_url=request.file_url,
            metadata={
                'interactive_config': request.interactive_config,
                'difficulty': request.difficulty_level
            }
        )

    @staticmethod
    def map_content_to_response(
        content: EducationalContent,
        author_name: str,
        rating: float
    ) -> ContentResponse:
        """Преобразует доменную модель контента в DTO ответа"""
        return ContentResponse(
            id=content.id,
            title=content.title,
            type=content.content_type,
            preview_url=content.file_url,
            author_name=author_name,
            rating=rating,
            difficulty=content.metadata.get('difficulty', 'medium'),
            interactive_available=bool(content.metadata.get('interactive_config')),
            created_at=content.created_at,
            grade_level=content.grade_level
        )

    @staticmethod
    def map_tutor_profile_to_response(
        profile: UserProfile,
        rating: float,
        completed_sessions: int
    ) -> TutorProfileResponse:
        """Преобразует профиль пользователя в DTO репетитора"""
        return TutorProfileResponse(
            tutor_id=profile.id,
            full_name=f"{profile.first_name} {profile.last_name}",
            subjects=profile.subjects,
            rating=rating,
            completed_sessions=completed_sessions,
            hourly_rate=profile.metadata.get('hourly_rate', 0),
            teaching_style=profile.metadata.get('teaching_style')
        )

    @staticmethod
    def map_learning_progress(progress: LearningProgress) -> dict:
        """Преобразует прогресс обучения в словарь для сериализации"""
        return {
            'content_id': str(progress.content_id),
            'score': progress.score,
            'completion_date': progress.completion_date.isoformat(),
            'attempts': progress.attempts
        }
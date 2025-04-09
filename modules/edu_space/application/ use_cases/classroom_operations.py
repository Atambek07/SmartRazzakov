# modules/edu_space/application/use_cases/classroom_operations.py
from uuid import UUID
from ...domain.entities import Course
from ...domain.repositories import CourseRepository
from ...domain.exceptions import EnrollmentError
from ..dto.classroom_dto import (
    CourseCreateRequest,
    CourseResponse,
    EnrollmentRequest
)

class ClassroomManager:
    def __init__(self, course_repo: CourseRepository):
        self.course_repo = course_repo

    def create_course(self, request: CourseCreateRequest) -> CourseResponse:
        course = Course(
            id=UUID(int=0),
            title=request.title,
            tutor_id=request.tutor_id,
            schedule=request.schedule,
            price=request.price,
            capacity=request.capacity
        )
        
        created_course = self.course_repo.save(course)
        return CourseResponse(
            id=created_course.id,
            title=created_course.title,
            tutor_name=self._get_tutor_name(created_course.tutor_id),
            schedule=created_course.schedule,
            enrolled_students=len(created_course.enrolled_students),
            available_seats=created_course.capacity - len(created_course.enrolled_students),
            rating=created_course.rating,
            price_display=f"{created_course.price} KZT"
        )

    def enroll_student(self, request: EnrollmentRequest):
        course = self.course_repo.get_by_id(request.course_id)
        
        if len(course.enrolled_students) >= course.capacity:
            raise EnrollmentError("Course is full")
            
        if request.student_id in course.enrolled_students:
            raise EnrollmentError("Already enrolled")
            
        course.enrolled_students.append(request.student_id)
        self.course_repo.save(course)

    def _get_tutor_name(self, tutor_id: UUID) -> str:
        # Implementation would call user service
        return "Tutor Name"
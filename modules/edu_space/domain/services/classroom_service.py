from abc import ABC, abstractmethod
from uuid import UUID
from ..entities import Course
from ..exceptions import EnrollmentError, CourseCapacityError, DuplicateEnrollmentError

class ClassroomService(ABC):
    @abstractmethod
    def create_course(self, course_data: dict) -> Course:
        """Создает новый учебный курс"""
        pass

    @abstractmethod
    def enroll_student(self, course_id: UUID, student_id: UUID):
        """Записывает студента на курс"""
        pass

    @abstractmethod
    def update_course_schedule(self, course_id: UUID, new_schedule: dict):
        """Обновляет расписание курса"""
        pass

class BaseClassroomService(ClassroomService):
    def __init__(self, course_repository):
        self.course_repo = course_repository

    def enroll_student(self, course_id: UUID, student_id: UUID):
        course = self.course_repo.get_by_id(course_id)
        
        if student_id in course.enrolled_students:
            raise DuplicateEnrollmentError("Student already enrolled")
            
        if len(course.enrolled_students) >= course.capacity:
            raise CourseCapacityError("Course is full")
            
        course.enrolled_students.append(student_id)
        self.course_repo.save(course)
        return course
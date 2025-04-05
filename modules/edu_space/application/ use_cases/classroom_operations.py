from ..domain.entities import VirtualClassroom
from ..domain.services.classroom_service import ClassroomService
from .dto.classroom_dto import CreateClassroomDTO


class ScheduleClassUseCase:
    def __init__(self, classroom_service: ClassroomService):
        self.service = classroom_service

    def execute(self, dto: CreateClassroomDTO) -> VirtualClassroom:
        """Создает виртуальный класс и настраивает видеоконференцию"""
        classroom = self.service.create_classroom(
            teacher_id=dto.teacher_id,
            student_ids=dto.student_ids,
            content_ids=dto.content_ids,
            schedule=dto.schedule
        )

        # Интеграция с Zoom
        if dto.video_conference:
            meeting = self.service.setup_video_conference(classroom.id)
            classroom.metadata['meeting_link'] = meeting['join_url']

        return classroom
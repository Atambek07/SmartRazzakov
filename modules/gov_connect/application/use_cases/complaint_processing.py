from ..domain.entities import CitizenComplaint
from ..domain.services import ComplaintWorkflow
from .dto.complaint_dto import SubmitComplaintDTO


class SubmitComplaintUseCase:
    def __init__(self, complaint_repository, workflow_engine: ComplaintWorkflow):
        self.repo = complaint_repository
        self.workflow = workflow_engine

    def execute(self, dto: SubmitComplaintDTO) -> CitizenComplaint:
        """Обрабатывает новую жалобу от гражданина"""
        complaint = CitizenComplaint(
            id=None,
            title=dto.title,
            description=dto.description,
            location=dto.location,
            photo_url=dto.photo_url,
            status="pending",
            priority="low",
            citizen_id=dto.citizen_id,
            created_at=dto.created_at
        )

        self.workflow.process_complaint(complaint)
        saved_complaint = self.repo.save(complaint)
        return saved_complaint
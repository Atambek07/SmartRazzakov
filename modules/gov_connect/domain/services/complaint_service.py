# modules/gov_connect/domain/services/complaint_service.py
from typing import List, Optional
from uuid import UUID
from ...domain.entities import Complaint, ComplaintStatus
from ...application.dto import ComplaintResponseDTO
from core.utils.logging import log_service

class ComplaintService:
    def __init__(self, repo, geo_service, notification_service):
        self.repo = repo
        self.geo_service = geo_service
        self.notifier = notification_service

    @log_service("Создание жалобы")
    def create_complaint(self, complaint_data: dict) -> Complaint:
        """Основной метод создания жалобы с валидацией"""
        if not self.geo_service.validate_coordinates(
            complaint_data['latitude'],
            complaint_data['longitude']
        ):
            raise ValueError("Invalid coordinates")

        complaint = Complaint(**complaint_data)
        return self.repo.save(complaint)

    def update_status(
        self,
        complaint_id: UUID,
        new_status: ComplaintStatus,
        comment: Optional[str] = None
    ) -> ComplaintResponseDTO:
        """Обновление статуса с нотификацией"""
        complaint = self.repo.find_by_id(complaint_id)
        if not complaint:
            raise ValueError("Complaint not found")

        old_status = complaint.status
        complaint.status = new_status
        updated = self.repo.update(complaint)

        if old_status != new_status:
            self._notify_status_change(updated, comment)

        return ComplaintResponseDTO.from_orm(updated)

    def find_similar_complaints(self, complaint: Complaint) -> List[Complaint]:
        """Поиск похожих жалоб по геолокации и категории"""
        return self.repo.find_by_criteria(
            latitude=complaint.latitude,
            longitude=complaint.longitude,
            category=complaint.category,
            max_distance=500,  # метров
            days_back=30
        )

    def _notify_status_change(self, complaint: Complaint, comment: str):
        """Внутренний метод отправки уведомлений"""
        message = {
            "complaint_id": str(complaint.id),
            "new_status": complaint.status.value,
            "comment": comment
        }
        self.notifier.send(
            recipient=complaint.user_id,
            message_type="STATUS_UPDATE",
            payload=message
        )
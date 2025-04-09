# modules/gov_connect/application/use_cases/complaint_processing.py
from typing import Optional
from uuid import UUID
from ...domain.entities import ComplaintEntity
from ...domain.services import ComplaintService, GeoService
from ...infrastructure.repositories import ComplaintRepository
from core.utils.responses import ResponseSuccess, ResponseFailure
from core.utils.logging import log_action

class ComplaintProcessingUseCase:
    def __init__(
        self, 
        repo: ComplaintRepository,
        service: ComplaintService,
        geo: GeoService
    ):
        self.repo = repo
        self.service = service
        self.geo = geo

    @log_action("Create Complaint")
    def create_complaint(self, dto) -> ResponseSuccess | ResponseFailure:
        try:
            # Валидация геоданных
            if not self.geo.validate_coordinates(dto.location):
                return ResponseFailure("Недопустимые координаты")

            # Создание entity
            complaint = ComplaintEntity(
                user_id=dto.user_id,
                title=dto.title,
                description=dto.description,
                location=dto.location,
                category=dto.category,
                photo_urls=dto.photo_urls,
                audio_url=dto.audio_url,
                anonymous=dto.anonymous
            )

            # Сохранение
            created = self.repo.create(complaint)
            
            # Поиск похожих жалоб
            similar = self.service.find_similar_complaints(created)
            if similar:
                self.repo.link_similar_complaints(created.id, [c.id for c in similar])

            return ResponseSuccess({
                "id": str(created.id),
                "tracking_code": created.tracking_code,
                "similar_found": len(similar)
            })
            
        except Exception as e:
            return ResponseFailure(f"Ошибка создания жалобы: {str(e)}")

class ComplaintStatusUpdateUseCase:
    def __init__(self, repo: ComplaintRepository, notification_service):
        self.repo = repo
        self.notifier = notification_service

    def update_status(self, complaint_id: UUID, new_status: str, comment: str = None):
        try:
            complaint = self.repo.get_by_id(complaint_id)
            if not complaint:
                return ResponseFailure("Жалоба не найдена")

            # Обновление статуса
            updated = self.repo.update_status(
                complaint_id, 
                new_status, 
                municipal_comment=comment
            )

            # Уведомление пользователя
            if not complaint.anonymous:
                self.notifier.send(
                    user_id=complaint.user_id,
                    message=f"Статус вашей жалобы {complaint.tracking_code} изменен на {new_status}"
                )

            return ResponseSuccess({
                "new_status": new_status,
                "updated_at": updated.updated_at
            })
        except Exception as e:
            return ResponseFailure(f"Ошибка обновления статуса: {str(e)}")

class ComplaintModerationUseCase:
    def __init__(self, repo: ComplaintRepository, ai_moderation_service):
        self.repo = repo
        self.ai = ai_moderation_service

    def moderate_content(self, complaint_id: UUID):
        try:
            complaint = self.repo.get_by_id(complaint_id)
            if not complaint:
                return ResponseFailure("Жалоба не найдена")

            # Анализ контента
            analysis = self.ai.analyze(
                text=complaint.description,
                images=complaint.photo_urls,
                audio=complaint.audio_url
            )

            # Автоматическая модерация
            if analysis['verdict'] == 'reject':
                self.repo.update_status(
                    complaint_id,
                    'rejected',
                    internal_comment=analysis['reason']
                )
            
            return ResponseSuccess(analysis)
        except Exception as e:
            return ResponseFailure(f"Ошибка модерации: {str(e)}")
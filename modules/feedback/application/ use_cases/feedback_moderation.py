# modules/feedback/application/use_cases/feedback_moderation.py
from abc import ABC, abstractmethod
from ...domain.entities import ReviewEntity
from ...application.dto import ReviewResponseDTO
from core.utils import BaseUseCase
from core.integrations import ModerationAPI, NotificationService

class ModerationRepository(ABC):
    @abstractmethod
    def update_status(self, review_id: int, status: str, comment: str = None):
        pass

class ModerateReviewUseCase(BaseUseCase):
    def __init__(self, 
                 repo: ModerationRepository,
                 moderation_api: ModerationAPI,
                 notifier: NotificationService):
        self.repo = repo
        self.moderation_api = moderation_api
        self.notifier = notifier

    def execute(self, review_id: int, moderator_id: int):
        # Проверка через AI модерацию
        review = self.repo.get(review_id)
        check_result = self.moderation_api.check_content(
            text=review.text,
            media=review.media
        )
        
        # Автоматическое решение
        if check_result['status'] == 'auto_approved':
            new_status = 'approved'
        elif check_result['status'] == 'auto_rejected':
            new_status = 'rejected'
        else:
            new_status = 'pending'
        
        # Сохранение статуса
        updated = self.repo.update_status(
            review_id=review_id,
            status=new_status,
            comment=check_result.get('reason')
        )
        
        # Уведомление автора
        if new_status != 'pending':
            self.notifier.send(
                user_id=review.author_id,
                template="review_status_changed",
                context={
                    "status": new_status,
                    "review_id": review_id,
                    "comment": check_result.get('reason')
                }
            )
        
        return ReviewResponseDTO.from_entity(updated)

class GenerateSummaryReportUseCase(BaseUseCase):
    def __init__(self, repo: ModerationRepository, analytics):
        self.repo = repo
        self.analytics = analytics

    def execute(self, period: dict):
        data = self.repo.get_moderation_stats(period)
        report = self.analytics.generate_moderation_report(data)
        
        return {
            "period": period,
            "total_reviews": report.total_reviews,
            "approved": report.approved,
            "rejected": report.rejected,
            "average_moderation_time": report.avg_time,
            "top_moderators": report.top_moderators
        }
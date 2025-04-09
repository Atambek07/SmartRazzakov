# modules/feedback/infrastructure/integrations/moderation/manual_moderation.py
from core.tasks import queue

class ManualModerationAdapter:
    def __init__(self, admin_group_id: int):
        self.admin_group_id = admin_group_id
    
    def create_moderation_task(self, review_id: int):
        """Постановка задачи в очередь модераторов"""
        queue.enqueue(
            'moderation_tasks',
            {
                "action": "moderate_review",
                "review_id": review_id
            },
            priority=2
        )
    
    def get_pending_tasks(self):
        """Получение списка задач для модерации"""
        return queue.get_tasks('moderation_tasks')
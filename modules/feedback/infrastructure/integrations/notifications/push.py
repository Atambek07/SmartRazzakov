# modules/feedback/infrastructure/integrations/notifications/push.py
from core.notifications import BaseNotifier

class PushNotifier(BaseNotifier):
    def send_review_update(self, user_id: int, message: dict):
        """Отправка push-уведомления"""
        payload = {
            "type": "review_status",
            "data": message
        }
        self._send_push(
            user_id=user_id,
            payload=payload,
            ttl=86400
        )
    
    def send_moderation_reminder(self, moderator_ids: list):
        """Напоминание модераторам о нерешенных задачах"""
        for user_id in moderator_ids:
            self._send_push(
                user_id=user_id,
                payload={"type": "moderation_reminder"},
                priority='high'
            )
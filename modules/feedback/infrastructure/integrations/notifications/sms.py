# modules/feedback/infrastructure/integrations/notifications/sms.py
from core.notifications import BaseNotifier

class SMSNotifier(BaseNotifier):
    def send_simple_sms(self, phone: str, message: str):
        """Отправка простого SMS"""
        self._send_sms(
            to=phone,
            body=message,
            sender="SmartRzzakov"
        )
    
    def send_review_confirmation(self, phone: str, review_id: int):
        """SMS с подтверждением принятия отзыва"""
        message = f"Ваш отзыв #{review_id} был успешно опубликован."
        self._send_sms(
            to=phone,
            body=message,
            sender="Feedback"
        )
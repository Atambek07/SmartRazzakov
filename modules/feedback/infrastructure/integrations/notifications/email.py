# modules/feedback/infrastructure/integrations/notifications/email.py
from core.notifications import BaseNotifier
from core.templates import render_template

class EmailNotifier(BaseNotifier):
    def send_review_status(self, user_email: str, context: dict):
        """Отправка email о изменении статуса отзыва"""
        subject = "Статус вашего отзыва изменен"
        body = render_template('emails/review_status.html', context)
        self._send_email(
            to=user_email,
            subject=subject,
            body=body,
            template_id="review-status-update"
        )

    def send_moderation_alert(self, moderator_emails: list, context: dict):
        """Уведомление модераторов о новой задаче"""
        subject = "Новая задача на модерацию"
        body = render_template('emails/new_moderation_task.html', context)
        for email in moderator_emails:
            self._send_email(
                to=email,
                subject=subject,
                body=body,
                priority='high'
            )
from django.core.mail import send_mail
from django.conf import settings
from twilio.rest import Client


class NotificationService:
    def __init__(self):
        self.twilio_client = Client(
            settings.TWILIO_ACCOUNT_SID,
            settings.TWILIO_AUTH_TOKEN
        )

    def send_complaint_update(self, complaint, recipient):
        """Отправляет уведомление об изменении статуса жалобы"""
        # Email уведомление
        send_mail(
            subject=f"Обновление по вашей жалобе #{complaint.id}",
            message=f"Статус: {complaint.get_status_display()}\nКомментарий: {complaint.resolution_comment}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[recipient.email]
        )

        # SMS уведомление
        if recipient.phone_number:
            self.twilio_client.messages.create(
                body=f"Ваша жалоба #{complaint.id} обновлена. Статус: {complaint.status}",
                from_=settings.TWILIO_PHONE_NUMBER,
                to=recipient.phone_number
            )
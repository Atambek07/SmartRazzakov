# modules/gov_connect/infrastructure/integrations/notification_system.py
from abc import ABC, abstractmethod
from typing import Dict, Any
import logging
from twilio.rest import Client
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from firebase_admin import messaging

logger = logging.getLogger(__name__)

class NotificationService(ABC):
    @abstractmethod
    def send(self, recipient: str, message: Dict[str, Any]):
        pass

class TwilioSMSNotifier(NotificationService):
    def __init__(self, account_sid: str, auth_token: str, from_number: str):
        self.client = Client(account_sid, auth_token)
        self.from_number = from_number

    def send(self, recipient: str, message: Dict[str, Any]):
        try:
            self.client.messages.create(
                body=message.get('text'),
                from_=self.from_number,
                to=recipient
            )
        except Exception as e:
            logger.error(f"SMS sending error: {str(e)}")
            raise

class SendGridEmailNotifier(NotificationService):
    def __init__(self, api_key: str):
        self.client = SendGridAPIClient(api_key)

    def send(self, recipient: str, message: Dict[str, Any]):
        try:
            mail = Mail(
                from_email=message.get('from', 'noreply@govconnect.kz'),
                to_emails=recipient,
                subject=message.get('subject', 'Уведомление GovConnect'),
                html_content=message.get('html')
            )
            self.client.send(mail)
        except Exception as e:
            logger.error(f"Email sending error: {str(e)}")
            raise

class FirebasePushNotifier(NotificationService):
    def send(self, recipient: str, message: Dict[str, Any]):
        try:
            notification = messaging.Notification(
                title=message.get('title'),
                body=message.get('body')
            )
            
            message = messaging.Message(
                notification=notification,
                token=recipient,
                data=message.get('data', {})
            )
            
            response = messaging.send(message)
            return response
        except Exception as e:
            logger.error(f"Push notification error: {str(e)}")
            raise
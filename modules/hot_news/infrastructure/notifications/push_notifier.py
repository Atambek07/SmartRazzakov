import os
from typing import List, Dict, Optional
from firebase_admin import messaging, initialize_app, exceptions
from core.utils.logging import get_logger
from core.config import settings
from .base_notifier import BaseNotifier

logger = get_logger(__name__)

class PushNotifier(BaseNotifier):
    def __init__(self):
        if not firebase_admin._apps:
            self.app = initialize_app(
                credential=credentials.Certificate(
                    settings.FIREBASE_CREDENTIALS
                )
            )
    
    async def send(
        self,
        user_id: str,
        message: Dict[str, Any],
        tokens: Optional[List[str]] = None,
        topic: Optional[str] = None
    ) -> bool:
        try:
            notification = messaging.Notification(
                title=message.get('title'),
                body=message.get('content')
            )
            
            data = {
                'category': message.get('category'),
                'priority': str(message.get('priority')),
                'deep_link': f"smartrazzakov://news/{message.get('id')}"
            }

            if topic:
                fcm_message = messaging.Message(
                    notification=notification,
                    data=data,
                    topic=topic
                )
            elif tokens:
                fcm_message = messaging.MulticastMessage(
                    notification=notification,
                    data=data,
                    tokens=tokens
                )
            else:
                fcm_message = messaging.Message(
                    notification=notification,
                    data=data,
                    token=self._get_user_token(user_id)
                )

            response = messaging.send(fcm_message)
            logger.info(f"Push sent: {response}")
            return True
        
        except exceptions.FirebaseError as e:
            logger.error(f"FCM error: {str(e)}")
            return False
        except Exception as e:
            logger.error(f"Push failed: {str(e)}")
            return False

    def _get_user_token(self, user_id: str) -> str:
        from modules.user_management.infrastructure.models import FCMTokenModel
        return FCMTokenModel.objects.filter(
            user_id=user_id,
            is_active=True
        ).latest('created_at').token
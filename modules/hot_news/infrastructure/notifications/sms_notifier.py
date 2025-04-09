from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException
from core.utils.logging import get_logger
from core.config import settings
from .base_notifier import BaseNotifier

logger = get_logger(__name__)

class SMSNotifier(BaseNotifier):
    def __init__(self):
        self.client = Client(
            settings.TWILIO_ACCOUNT_SID,
            settings.TWILIO_AUTH_TOKEN
        )
        self.from_number = settings.TWILIO_PHONE_NUMBER
    
    async def send(
        self,
        user_id: str,
        message: Dict[str, Any],
        phone: Optional[str] = None
    ) -> bool:
        try:
            if not phone:
                phone = self._get_user_phone(user_id)
            
            content = f"{message.get('title')}\n{message.get('content')}"
            
            if settings.DEBUG:
                logger.debug(f"SMS mock: {content}")
                return True

            self.client.messages.create(
                body=content,
                from_=self.from_number,
                to=self._format_phone(phone)
            )
            return True
        
        except TwilioRestException as e:
            logger.error(f"SMS failed: {e.msg}")
            return False
        except Exception as e:
            logger.error(f"SMS error: {str(e)}")
            return False

    def _get_user_phone(self, user_id: str) -> str:
        from modules.user_management.infrastructure.models import UserProfileModel
        return UserProfileModel.objects.get(
            user_id=user_id
        ).phone_number
    
    def _format_phone(self, phone: str) -> str:
        return f"+{phone.lstrip('+')}"
# modules/community_hub/infrastructure/integrations/realtime/firebase.py
import firebase_admin
from firebase_admin import messaging
from .. import BaseRealtimeClient

class FirebaseNotificationClient(BaseRealtimeClient):
    def __init__(self, cred_path: str):
        self.cred = firebase_admin.credentials.Certificate(cred_path)
        self.app = firebase_admin.initialize_app(self.cred)

    async def send_notification(
        self,
        device_tokens: List[str],
        title: str,
        body: str,
        data: Dict = None
    ):
        message = messaging.MulticastMessage(
            notification=messaging.Notification(title=title, body=body),
            data=data or {},
            tokens=device_tokens
        )
        response = messaging.send_multicast(message)
        return response.success_count

    @property
    def is_connected(self) -> bool:
        return self.app is not None

    async def connect(self):
        pass  # Firebase инициализируется при создании

    async def disconnect(self):
        firebase_admin.delete_app(self.app)
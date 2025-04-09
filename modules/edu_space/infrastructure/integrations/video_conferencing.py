from abc import ABC, abstractmethod
from typing import Dict, Optional
from datetime import datetime, timedelta
import httpx
from django.conf import settings

class VideoConferenceError(Exception):
    """Базовое исключение для ошибок видеоконференций"""
    def __init__(self, message: str, code: str):
        super().__init__(message)
        self.code = code

class BaseVideoService(ABC):
    @abstractmethod
    async def create_meeting(
        self,
        title: str,
        start_time: datetime,
        duration: int,
        password: Optional[str] = None
    ) -> Dict:
        pass

    @abstractmethod
    async def get_meeting_link(self, meeting_id: str) -> str:
        pass

class ZoomService(BaseVideoService):
    def __init__(self):
        self.base_url = "https://api.zoom.us/v2"
        self.headers = {
            "Authorization": f"Bearer {self._get_access_token()}",
            "Content-Type": "application/json"
        }

    def _get_access_token(self):
        # Получение OAuth токена для Zoom
        response = httpx.post(
            "https://zoom.us/oauth/token",
            params={
                "grant_type": "account_credentials",
                "account_id": settings.ZOOM_ACCOUNT_ID
            },
            auth=(settings.ZOOM_CLIENT_ID, settings.ZOOM_CLIENT_SECRET)
        )
        return response.json()["access_token"]

    async def create_meeting(self, title, start_time, duration, password=None):
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/users/me/meetings",
                json={
                    "topic": title,
                    "type": 2,
                    "start_time": start_time.isoformat(),
                    "duration": duration,
                    "password": password or "",
                    "settings": {
                        "host_video": True,
                        "participant_video": True,
                        "join_before_host": False
                    }
                },
                headers=self.headers
            )
            if response.status_code != 201:
                raise VideoConferenceError(
                    f"Zoom API error: {response.text}",
                    code="ZOOM_API_ERROR"
                )
            data = response.json()
            return {
                "id": data["id"],
                "join_url": data["join_url"],
                "password": data["password"]
            }

    async def get_meeting_link(self, meeting_id):
        return f"https://zoom.us/j/{meeting_id}"

class GoogleMeetService(BaseVideoService):
    async def create_meeting(self, title, start_time, duration, password=None):
        # Интеграция с Google Calendar API
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://www.googleapis.com/calendar/v3/calendars/primary/events",
                headers={
                    "Authorization": f"Bearer {settings.GOOGLE_ACCESS_TOKEN}"
                },
                json={
                    "summary": title,
                    "start": {"dateTime": start_time.isoformat()},
                    "end": {"dateTime": (start_time + timedelta(minutes=duration)).isoformat()},
                    "conferenceData": {
                        "createRequest": {"requestId": "edu-space-meeting"}
                    }
                }
            )
            data = response.json()
            return {
                "id": data["id"],
                "join_url": data["hangoutLink"],
                "password": ""
            }

    async def get_meeting_link(self, meeting_id):
        return f"https://meet.google.com/{meeting_id}"

class VideoServiceFactory:
    @staticmethod
    def get_service(name: str = "zoom") -> BaseVideoService:
        services = {
            "zoom": ZoomService,
            "google": GoogleMeetService
        }
        return services[name.lower()]()
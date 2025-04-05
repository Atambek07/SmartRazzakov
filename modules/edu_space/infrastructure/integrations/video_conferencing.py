import requests
from django.conf import settings


class ZoomIntegration:
    def __init__(self):
        self.api_key = settings.ZOOM_API_KEY
        self.api_secret = settings.ZOOM_API_SECRET
        self.base_url = "https://api.zoom.us/v2"

    def create_meeting(self, topic: str, duration: int) -> dict:
        """Создает Zoom-конференцию для виртуального класса"""
        headers = {
            "Authorization": f"Bearer {self._generate_jwt()}",
            "Content-Type": "application/json"
        }
        payload = {
            "topic": topic,
            "type": 2,  # Scheduled meeting
            "duration": duration,
            "settings": {
                "host_video": True,
                "participant_video": True,
                "join_before_host": False
            }
        }

        response = requests.post(
            f"{self.base_url}/users/me/meetings",
            headers=headers,
            json=payload
        )

        if response.status_code != 201:
            raise ConnectionError("Failed to create Zoom meeting")

        return response.json()
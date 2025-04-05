from twilio.rest import Client
from django.conf import settings

class VideoConsultationService:
    def __init__(self):
        self.client = Client(settings.TWILIO_SID, settings.TWILIO_TOKEN)

    def create_room(self, doctor_id: str, patient_id: str) -> dict:
        """Создает видеокомнату для консультации"""
        room = self.client.video.rooms.create(
            unique_name=f"consult_{doctor_id}_{patient_id}",
            type='peer-to-peer'
        )
        return {
            'room_sid': room.sid,
            'doctor_url': f"{settings.TWILIO_VIDEO_URL}/{room.sid}?user=doctor",
            'patient_url': f"{settings.TWILIO_VIDEO_URL}/{room.sid}?user=patient"
        }
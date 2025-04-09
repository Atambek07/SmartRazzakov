# modules/health_connect/domain/services/telemedicine.py
from datetime import datetime
from typing import Optional
from ....core.integrations.video import VideoConferenceClient
from ....core.integrations.chat import ChatServiceAdapter
from ..entities import Appointment
from ..exceptions import TelemedicineException

class TelemedicineService:
    def __init__(self,
                 video_client: VideoConferenceClient,
                 chat_service: ChatServiceAdapter,
                 appointment_service: AppointmentService):
        self.video = video_client
        self.chat = chat_service
        self.appointments = appointment_service

    def start_video_consultation(self, appointment_id: str) -> dict:
        """Инициализация видеоконсультации"""
        appointment = self.appointments.get_appointment(appointment_id)
        
        if appointment.status != AppointmentStatus.CONFIRMED:
            raise TelemedicineException("Appointment not confirmed")
        
        consultation = self.video.create_room(
            participants=[
                appointment.patient_id,
                appointment.provider_id
            ],
            duration=30  # minutes
        )
        
        self._create_chat_channel(appointment)
        return consultation

    def send_medical_files(self, appointment_id: str, files: list) -> None:
        """Обмен файлами во время консультации"""
        appointment = self.appointments.get_appointment(appointment_id)
        channel_id = f"chat_{appointment_id}"
        
        for file in files:
            self.chat.send_file(
                channel_id=channel_id,
                file=file,
                metadata={
                    'appointment_id': appointment_id,
                    'sender': file.sender_id
                }
            )

    def _create_chat_channel(self, appointment: Appointment) -> None:
        """Создание защищенного чата для консультации"""
        self.chat.create_channel(
            channel_id=f"chat_{appointment.id}",
            participants=[
                appointment.patient_id,
                appointment.provider_id
            ],
            encryption=True,
            retention_period=30  # days
        )

    def generate_consultation_report(self, appointment_id: str) -> dict:
        """Генерация отчета по завершении консультации"""
        appointment = self.appointments.get_appointment(appointment_id)
        transcript = self.chat.get_transcript(f"chat_{appointment_id}")
        recordings = self.video.get_recordings(appointment_id)
        
        return {
            "summary": self._generate_ai_summary(transcript),
            "diagnosis": None,  # To be filled by doctor
            "recommendations": None,
            "media": recordings
        }

    def _generate_ai_summary(self, transcript: str) -> str:
        """Использование ИИ для генерации краткого содержания"""
        ai_client = MedicalAIClient()
        return ai_client.summarize_consultation(transcript)
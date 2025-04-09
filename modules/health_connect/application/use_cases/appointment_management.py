# modules/health_connect/application/use_cases/appointment_management.py
from datetime import datetime
from typing import Optional
from ...domain.entities import Appointment, AppointmentStatus
from ...domain.services.appointment_service import AppointmentService
from ..dto.appointment_dto import (
    AppointmentCreate,
    AppointmentUpdate,
    AppointmentResponse,
    AppointmentSearch
)
from ..mappers import appointment_mapper
from core.utils import ApplicationResponse, LoggingService

class AppointmentUseCases:
    def __init__(self, 
                 appointment_service: AppointmentService,
                 logger: LoggingService):
        self.appointment_service = appointment_service
        self.logger = logger

class CreateAppointmentUseCase(AppointmentUseCases):
    def execute(self, dto: AppointmentCreate) -> ApplicationResponse:
        try:
            if not self._check_provider_availability(dto.provider_id, dto.scheduled_time):
                return ApplicationResponse.error("Provider not available", code=409)
            
            appointment = appointment_mapper.dto_to_entity(dto)
            created = self.appointment_service.create_appointment(appointment)
            return ApplicationResponse.success(
                appointment_mapper.entity_to_dto(created)
            )
        
        except AppointmentConflict as e:
            self.logger.warning(f"Appointment conflict: {str(e)}")
            return ApplicationResponse.error(str(e), code=409)
        
        except ProviderNotAvailable:
            return ApplicationResponse.error("Provider not available", code=409)

    def _check_provider_availability(self, provider_id: str, time: datetime) -> bool:
        # Интеграция с календарем провайдера
        return self.appointment_service.check_availability(provider_id, time)

class CancelAppointmentUseCase(AppointmentUseCases):
    def execute(self, appointment_id: str, user_id: str) -> ApplicationResponse:
        try:
            appointment = self.appointment_service.get_appointment(appointment_id)
            
            if appointment.patient_id != user_id:
                return ApplicationResponse.error("Permission denied", code=403)
            
            self.appointment_service.cancel_appointment(appointment_id)
            return ApplicationResponse.success(None, message="Appointment cancelled")
        
        except MedicalRecordNotFound:
            return ApplicationResponse.error("Appointment not found", code=404)

class ConfirmAppointmentUseCase(AppointmentUseCases):
    def execute(self, appointment_id: str) -> ApplicationResponse:
        try:
            confirmed = self.appointment_service.confirm_appointment(appointment_id)
            # Интеграция с системой уведомлений
            self._send_confirmation_notification(confirmed)
            return ApplicationResponse.success(
                appointment_mapper.entity_to_dto(confirmed)
            )
        
        except MedicalRecordNotFound:
            return ApplicationResponse.error("Appointment not found", code=404)
        
    def _send_confirmation_notification(self, appointment: Appointment):
        # Интеграция с модулем уведомлений
        notification_service = NotificationClient()
        notification_service.send(
            user_id=appointment.patient_id,
            type="APPOINTMENT_CONFIRMATION",
            data={
                "provider": appointment.provider_id,
                "time": appointment.scheduled_time
            }
        )   
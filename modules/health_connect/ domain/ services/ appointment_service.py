# modules/health_connect/domain/services/appointment_service.py
from datetime import datetime, timedelta
from typing import Optional, List
from ...entities import Appointment, AppointmentStatus
from ....core.utils.logging import LoggingService
from ....core.integrations.calendar import CalendarAdapter
from ..exceptions import AppointmentConflict, ProviderNotAvailable

class AppointmentService:
    def __init__(self, 
                 repository: 'AppointmentRepository',
                 calendar_adapter: CalendarAdapter,
                 logger: LoggingService):
        self.repo = repository
        self.calendar = calendar_adapter
        self.logger = logger

    def create_appointment(self, appointment: Appointment) -> Appointment:
        """Создание новой записи с проверкой конфликтов"""
        if not self._is_time_slot_available(appointment.provider_id, 
                                          appointment.scheduled_time):
            raise AppointmentConflict("Time slot already booked")

        if self._has_pending_appointments(appointment.patient_id):
            raise AppointmentConflict("Patient has pending appointments")

        return self.repo.save(appointment)

    def cancel_appointment(self, appointment_id: str) -> None:
        """Отмена записи с уведомлениями"""
        appointment = self.repo.get_by_id(appointment_id)
        if appointment.status == AppointmentStatus.CANCELLED:
            return

        updated = appointment.copy(update={
            'status': AppointmentStatus.CANCELLED,
            'modified_at': datetime.now()
        })
        self.repo.save(updated)
        self._notify_cancellation(appointment)

    def confirm_appointment(self, appointment_id: str) -> Appointment:
        """Подтверждение записи врачом"""
        appointment = self.repo.get_by_id(appointment_id)
        if appointment.status != AppointmentStatus.PENDING:
            raise ValueError("Only pending appointments can be confirmed")

        confirmed = appointment.copy(update={
            'status': AppointmentStatus.CONFIRMED,
            'modified_at': datetime.now()
        })
        return self.repo.save(confirmed)

    def _is_time_slot_available(self, provider_id: str, time: datetime) -> bool:
        """Проверка доступности временного слота у врача"""
        return self.calendar.check_availability(
            provider_id=provider_id,
            start=time - timedelta(minutes=15),
            end=time + timedelta(minutes=45)
        )

    def _has_pending_appointments(self, patient_id: str) -> bool:
        """Проверка наличия неподтвержденных записей у пациента"""
        return len(self.repo.get_patient_appointments(
            patient_id,
            statuses=[AppointmentStatus.PENDING]
        )) >= 2

    def _notify_cancellation(self, appointment: Appointment) -> None:
        """Интеграция с системой уведомлений"""
        notification_service = NotificationClient()
        notification_service.send(
            user_id=appointment.patient_id,
            type="APPOINTMENT_CANCELLED",
            data={
                "appointment_id": appointment.id,
                "original_time": appointment.scheduled_time
            }
        )
# modules/health_connect/infrastructure/repositories/medical_repo.py
from django.db import transaction
from typing import List, Optional
from ..models.medical import MedicalRecord as MedicalRecordModel
from ..models.medical import Appointment as AppointmentModel
from ...domain.entities import MedicalRecord, Appointment
from ...domain.exceptions import MedicalRecordNotFound, AppointmentConflict
from core.utils.logging import LoggingService

class MedicalRepository:
    def __init__(self, logger: LoggingService):
        self.logger = logger

    @transaction.atomic
    def save_record(self, record: MedicalRecord) -> MedicalRecord:
        try:
            model, created = MedicalRecordModel.objects.update_or_create(
                id=record.id,
                defaults={
                    'patient_id': record.patient_id,
                    'record_type': record.record_type.value,
                    'title': record.title,
                    'content': record.content,
                    'provider_id': record.provider_id,
                    'is_confidential': record.is_confidential,
                    'related_appointment_id': record.related_appointment
                }
            )
            return self._model_to_entity(model)
        except Exception as e:
            self.logger.error(f"Error saving medical record: {str(e)}")
            raise

    def get_record(self, record_id: str) -> MedicalRecord:
        try:
            model = MedicalRecordModel.objects.get(id=record_id)
            return self._model_to_entity(model)
        except MedicalRecordModel.DoesNotExist:
            raise MedicalRecordNotFound(record_id)

    def search_records(self, patient_id: str, **filters) -> List[MedicalRecord]:
        query = MedicalRecordModel.objects.filter(patient_id=patient_id)
        
        if 'record_type' in filters:
            query = query.filter(record_type=filters['record_type'])
        
        if 'start_date' in filters:
            query = query.filter(created_at__gte=filters['start_date'])
        
        if 'end_date' in filters:
            query = query.filter(created_at__lte=filters['end_date'])
        
        return [self._model_to_entity(m) for m in query.order_by('-created_at')]

    def _model_to_entity(self, model: MedicalRecordModel) -> MedicalRecord:
        return MedicalRecord(
            id=model.id,
            patient_id=model.patient_id,
            record_type=model.record_type,
            title=model.title,
            content=model.content,
            provider_id=model.provider_id,
            is_confidential=model.is_confidential,
            created_at=model.created_at,
            updated_at=model.updated_at,
            related_appointment=model.related_appointment_id
        )

class AppointmentRepository:
    def __init__(self, logger: LoggingService):
        self.logger = logger

    @transaction.atomic
    def save_appointment(self, appointment: Appointment) -> Appointment:
        try:
            model, created = AppointmentModel.objects.update_or_create(
                id=appointment.id,
                defaults={
                    'patient_id': appointment.patient_id,
                    'provider_id': appointment.provider_id,
                    'scheduled_time': appointment.scheduled_time,
                    'status': appointment.status.value,
                    'duration': appointment.duration,
                    'reason': appointment.reason,
                    'video_link': appointment.video_link
                }
            )
            return self._model_to_entity(model)
        except Exception as e:
            self.logger.error(f"Error saving appointment: {str(e)}")
            raise AppointmentConflict()

    def get_appointment(self, appointment_id: str) -> Appointment:
        try:
            model = AppointmentModel.objects.get(id=appointment_id)
            return self._model_to_entity(model)
        except AppointmentModel.DoesNotExist:
            raise MedicalRecordNotFound(appointment_id)

    def _model_to_entity(self, model: AppointmentModel) -> Appointment:
        return Appointment(
            id=model.id,
            patient_id=model.patient_id,
            provider_id=model.provider_id,
            scheduled_time=model.scheduled_time,
            status=model.status,
            duration=model.duration,
            reason=model.reason,
            video_link=model.video_link,
            created_at=model.created_at,
            updated_at=model.updated_at
        )
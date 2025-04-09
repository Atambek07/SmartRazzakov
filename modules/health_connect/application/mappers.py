# modules/health_connect/application/mappers.py
from datetime import datetime
from typing import Optional, Dict, Any
from .dto import *
from ..domain.entities import *

class MedicalRecordMapper:
    @staticmethod
    def dto_to_entity(dto: MedicalRecordCreate) -> MedicalRecord:
        """Convert creation DTO to domain entity"""
        return MedicalRecord(
            patient_id=dto.patient_id,
            record_type=dto.record_type,
            title=dto.title,
            description=dto.description,
            date=dto.date,
            provider_id=dto.provider_id,
            attachments=dto.attachments.copy(),
            is_confidential=dto.is_confidential,
            created_at=datetime.now(),
            modified_at=None
        )

    @staticmethod
    def entity_to_dto(entity: MedicalRecord) -> MedicalRecordResponse:
        """Convert domain entity to response DTO"""
        return MedicalRecordResponse(
            id=entity.id,
            patient_id=entity.patient_id,
            record_type=entity.record_type,
            title=entity.title,
            description=entity.description,
            date=entity.date,
            provider_id=entity.provider_id,
            attachments=entity.attachments.copy(),
            is_confidential=entity.is_confidential,
            created_at=entity.created_at,
            modified_at=entity.modified_at
        )

    @staticmethod
    def update_entity(entity: MedicalRecord, dto: MedicalRecordUpdate) -> MedicalRecord:
        """Apply update DTO to existing entity"""
        updated_fields = {}
        for field in dto.__fields_set__:
            value = getattr(dto, field)
            
            if field == 'attachments':
                updated_fields[field] = value.copy()
            else:
                updated_fields[field] = value
        
        return MedicalRecord(
            **{**entity.dict(), **updated_fields},
            modified_at=datetime.now()
        )

class AppointmentMapper:
    @staticmethod
    def dto_to_entity(dto: AppointmentCreate) -> Appointment:
        """Convert creation DTO to domain entity"""
        return Appointment(
            patient_id=dto.patient_id,
            provider_id=dto.provider_id,
            scheduled_time=dto.scheduled_time,
            reason=dto.reason,
            notes=dto.notes,
            status=AppointmentStatus.PENDING,
            created_at=datetime.now()
        )

    @staticmethod
    def entity_to_dto(entity: Appointment) -> AppointmentResponse:
        """Convert domain entity to response DTO"""
        return AppointmentResponse(
            id=entity.id,
            patient_id=entity.patient_id,
            provider_id=entity.provider_id,
            scheduled_time=entity.scheduled_time,
            status=entity.status,
            reason=entity.reason,
            notes=entity.notes,
            created_at=entity.created_at,
            modified_at=entity.modified_at
        )

    @staticmethod
    def update_entity(entity: Appointment, dto: AppointmentUpdate) -> Appointment:
        """Apply update DTO to existing entity"""
        updates = {}
        for field in dto.__fields_set__:
            value = getattr(dto, field)
            
            if field == 'scheduled_time' and value <= datetime.now():
                raise ValueError("Appointment time must be in future")
            
            updates[field] = value
        
        return Appointment(
            **{**entity.dict(), **updates},
            modified_at=datetime.now()
        )

class ProviderMapper:
    @staticmethod
    def entity_to_search_result(entity: HealthcareProvider) -> Dict[str, Any]:
        """Convert provider entity to emergency search result format"""
        return {
            "id": entity.id,
            "name": entity.name,
            "specialization": entity.specialization,
            "contact_info": entity.contact_info,
            "available_now": entity.is_available(datetime.now()),
            "languages": entity.languages.copy()
        }

class EmergencyMapper:
    @staticmethod
    def dto_to_alert(dto: EmergencyAlertDTO) -> Dict[str, Any]:
        """Convert emergency DTO to internal alert format"""
        return {
            "patient_id": dto.patient_id,
            "location": dto.location,
            "emergency_type": dto.emergency_type,
            "timestamp": dto.timestamp,
            "severity": dto.severity,
            "metadata": {
                "related_records": dto.related_records,
                "device_id": dto.device_id
            }
        }

# Инициализация мапперов для использования в Use Cases
medical_mapper = MedicalRecordMapper()
appointment_mapper = AppointmentMapper()
provider_mapper = ProviderMapper()
emergency_mapper = EmergencyMapper()
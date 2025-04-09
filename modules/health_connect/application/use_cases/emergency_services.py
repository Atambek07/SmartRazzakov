# modules/health_connect/application/use_cases/emergency_services.py
from typing import List
from ...domain.entities import HealthcareProvider
from ...domain.services import MedicalDataService, AppointmentService
from ..dto.medical_dto import EmergencyAlertDTO
from core.utils import ApplicationResponse, LoggingService
from core.integrations.sms import SMSClient
from modules.gov_connect.infrastructure.integrations import EmergencyGISService

class EmergencyUseCases:
    def __init__(self,
                 medical_data: MedicalDataService,
                 appointment_service: AppointmentService,
                 gis_service: EmergencyGISService,
                 sms_client: SMSClient,
                 logger: LoggingService):
        self.medical_data = medical_data
        self.appointments = appointment_service
        self.gis = gis_service
        self.sms = sms_client
        self.logger = logger

class TriggerEmergencyUseCase(EmergencyUseCases):
    def execute(self, alert: EmergencyAlertDTO) -> ApplicationResponse:
        try:
            # 1. Получить критическую медицинскую информацию
            records = self.medical_data.get_critical_records(alert.patient_id)
            
            # 2. Найти ближайших провайдеров
            providers = self.gis.find_nearest_providers(
                alert.location,
                types=['emergency']
            )
            
            # 3. Создать экстренную запись
            emergency_appointment = self._create_emergency_appointment(
                alert, 
                providers[0].id if providers else None
            )
            
            # 4. Уведомить экстренные службы
            self._notify_emergency_services(alert, providers)
            
            return ApplicationResponse.success({
                "emergency_id": emergency_appointment.id,
                "assigned_provider": providers[0].id if providers else None
            })
        
        except Exception as e:
            self.logger.emergency(f"Emergency failed: {str(e)}")
            return ApplicationResponse.error("Emergency processing failed", code=500)

    def _create_emergency_appointment(self, alert: EmergencyAlertDTO, provider_id: Optional[str]):
        return self.appointments.create_emergency_appointment(
            patient_id=alert.patient_id,
            provider_id=provider_id,
            emergency_type=alert.emergency_type,
            location=alert.location
        )

    def _notify_emergency_services(self, alert: EmergencyAlertDTO, providers: List[HealthcareProvider]):
        message = f"EMERGENCY ALERT: {alert.emergency_type} at {alert.location}"
        for provider in providers[:3]:  # Уведомляем 3 ближайших провайдера
            self.sms.send(
                phone=provider.contact_info,
                message=message
            )

class FindEmergencyProvidersUseCase(EmergencyUseCases):
    def execute(self, location: str) -> ApplicationResponse:
        providers = self.gis.find_nearest_providers(
            location,
            max_distance_km=5,
            types=['emergency', 'trauma']
        )
        return ApplicationResponse.success([
            {
                "id": p.id,
                "name": p.name,
                "specialization": p.specialization,
                "distance": p.distance,
                "eta": p.estimated_arrival_time
            } for p in providers
        ])
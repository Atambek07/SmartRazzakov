# modules/health_connect/__init__.py
"""
Инициализация модуля HealthConnect

Экспортирует основные компоненты для внешнего использования:
- Модели данных
- Сервисы
- API представления
"""

from .infrastructure.models import (
    PatientProfile,
    HealthcareProviderProfile,
    MedicalRecord,
    Appointment,
    MedicalFacility
)
from .application.services import (
    MedicalDataService,
    AppointmentService,
    TelemedicineService
)

__all__ = [
    # Модели
    'PatientProfile',
    'HealthcareProviderProfile',
    'MedicalRecord',
    'Appointment',
    'MedicalFacility',
    
    # Сервисы
    'MedicalDataService',
    'AppointmentService',
    'TelemedicineService',
    
    # API компоненты
    'MedicalRecordViewSet',
    'PatientAppointmentViewSet',
    'DoctorScheduleAPIView'
]

# Инициализация логгера модуля
import logging
logger = logging.getLogger(__name__)
logger.info("HealthConnect module initialized")
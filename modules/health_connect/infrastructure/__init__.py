# modules/health_connect/infrastructure/__init__.py
"""
Инициализация инфраструктурного слоя для модуля HealthConnect

Экспортирует основные компоненты для работы с:
- Медицинскими данными
- Внешними интеграциями
- Репозиториями данных
"""

from .integrations import (
    HL7Parser,
    FHIRAdapter,
    TwilioVideoProvider,
    WebRTCSignaling,
    MediaConfiguration
)
from .models import (
    PatientProfile,
    HealthcareProviderProfile,
    MedicalRecord,
    Appointment,
    MedicalFacility
)
from .repositories import (
    MedicalRepository,
    AppointmentRepository,
    UserRepository
)

__all__ = [
    # Интеграции
    'HL7Parser',
    'FHIRAdapter',
    'TwilioVideoProvider',
    'WebRTCSignaling',
    'MediaConfiguration',
    
    # Модели данных
    'PatientProfile',
    'HealthcareProviderProfile',
    'MedicalRecord',
    'Appointment',
    'MedicalFacility',
    
    # Репозитории
    'MedicalRepository',
    'AppointmentRepository',
    'UserRepository'
]

# Инициализация логгера по умолчанию
from core.utils.logging import get_logger
logger = get_logger(__name__)

def init_healthconnect_infrastructure():
    """Инициализация инфраструктурных компонентов при старте приложения"""
    logger.info("Initializing HealthConnect infrastructure layer...")
    # Здесь можно добавить код инициализации подключений к внешним сервисам
    # Например: проверка доступности HL7/FHIR серверов
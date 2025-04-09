# modules/health_connect/application/dto/__init__.py
from .medical_dto import *
from .appointment_dto import *

__all__ = [
    'MedicalRecordCreate',
    'MedicalRecordUpdate',
    'MedicalRecordResponse',
    'AppointmentCreate',
    'AppointmentUpdate',
    'AppointmentResponse',
    'AppointmentSearch',
    'MedicalRecordSearch'
]
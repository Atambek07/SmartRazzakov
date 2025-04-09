# modules/health_connect/presentation/serializers/__init__.py
from .medical_serializers import *
from .appointment_serializers import *

__all__ = [
    'MedicalRecordCreateSerializer',
    'MedicalRecordUpdateSerializer',
    'MedicalRecordResponseSerializer',
    'AppointmentCreateSerializer',
    'AppointmentUpdateSerializer',
    'AppointmentResponseSerializer'
]
# modules/gov_connect/presentation/serializers/__init__.py
"""
Сериализаторы для API GovConnect

Экспортирует:
- Complaint сериализаторы
- Service сериализаторы
"""
from .complaint_serializers import (
    ComplaintCreateSerializer,
    ComplaintUpdateSerializer,
    ComplaintDetailSerializer,
    ComplaintPhotoSerializer
)
from .service_serializers import (
    ServiceCategorySerializer,
    GovernmentServiceSerializer,
    BookingSlotSerializer
)

__all__ = [
    'ComplaintCreateSerializer',
    'ComplaintUpdateSerializer',
    'ComplaintDetailSerializer',
    'ComplaintPhotoSerializer',
    'ServiceCategorySerializer',
    'GovernmentServiceSerializer',
    'BookingSlotSerializer'
]
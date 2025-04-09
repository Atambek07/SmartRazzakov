# modules/gov_connect/infrastructure/models/__init__.py
"""
Модели данных для модуля GovConnect

Содержит:
- Complaint: Модель для хранения жалоб
- Service: Модель госуслуг
"""

from .complaints import Complaint, ComplaintPhoto
from .services import GovernmentService, ServiceCategory

__all__ = [
    'Complaint',
    'ComplaintPhoto',
    'GovernmentService',
    'ServiceCategory'
]
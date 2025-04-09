# modules/gov_connect/infrastructure/repositories/__init__.py
"""
Репозитории для работы с данными GovConnect

Содержит реализации:
- ComplaintRepository: Управление жалобами
- ServiceRepository: Работа с госуслугами
"""

from .complaint_repo import DjangoComplaintRepository
from .service_repo import DjangoServiceRepository

__all__ = [
    'DjangoComplaintRepository',
    'DjangoServiceRepository'
]
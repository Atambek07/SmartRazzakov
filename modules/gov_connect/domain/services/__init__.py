# modules/gov_connect/domain/services/__init__.py
"""
Сервисный слой модуля GovConnect

Содержит ядро бизнес-логики:
- ComplaintService: Управление жизненным циклом жалоб
- DocumentService: Работа с документами и отчетами
- WorkflowEngine: Автоматизация рабочих процессов
"""

from .complaint_service import ComplaintService
from .document_service import DocumentService
from .workflow_engine import WorkflowEngine

__all__ = [
    'ComplaintService',
    'DocumentService',
    'WorkflowEngine'
]
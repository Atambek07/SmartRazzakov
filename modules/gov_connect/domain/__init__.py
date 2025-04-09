# modules/gov_connect/domain/__init__.py
"""
Доменный слой модуля GovConnect

Экспортирует:
- Бизнес-сущности
- Value Objects
- Исключения доменного уровня
"""

from .entities import (
    Complaint,
    Booking,
    Voting,
    Document,
    ComplaintStatus,
    BookingStatus,
    VotingStatus
)

from .exceptions import (
    GovConnectError,
    InvalidGeoDataError,
    ComplaintNotFoundError,
    BookingConflictError,
    VotingPermissionError,
    WorkflowTransitionError,
    DocumentValidationError
)

__all__ = [
    # Entities
    'Complaint',
    'Booking',
    'Voting',
    'Document',
    
    # Enums
    'ComplaintStatus',
    'BookingStatus',
    'VotingStatus',
    
    # Exceptions
    'GovConnectError',
    'InvalidGeoDataError',                              
    'ComplaintNotFoundError',
    'BookingConflictError',
    'VotingPermissionError',
    'WorkflowTransitionError',
    'DocumentValidationError'
]
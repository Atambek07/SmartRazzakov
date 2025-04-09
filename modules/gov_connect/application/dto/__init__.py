# modules/gov_connect/application/dto/__init__.py
"""
Data Transfer Objects модуля GovConnect
"""
from .booking_dto import (
    BookingCreateDTO,
    BookingUpdateDTO,
    BookingResponseDTO,
    SlotAvailabilityDTO
)
from .complaint_dto import (
    ComplaintBaseDTO,
    ComplaintCreateDTO,
    ComplaintUpdateDTO,
    ComplaintResponseDTO,
    ComplaintStatusDTO
)

__all__ = [
    'BookingCreateDTO',
    'BookingUpdateDTO',
    'BookingResponseDTO',
    'SlotAvailabilityDTO',
    'ComplaintBaseDTO',
    'ComplaintCreateDTO',
    'ComplaintUpdateDTO',
    'ComplaintResponseDTO',
    'ComplaintStatusDTO'
]
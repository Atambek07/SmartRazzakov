# modules/gov_connect/infrastructure/repositories/service_repo.py
from datetime import datetime
from typing import List, Optional
from uuid import UUID
from django.db import transaction
from ...domain.entities import Booking as DomainBooking
from ...domain.exceptions import BookingConflictError
from ..models import GovernmentService, Booking
import logging

logger = logging.getLogger(__name__)

class DjangoServiceRepository:
    @transaction.atomic
    def create_booking(self, booking: DomainBooking) -> DomainBooking:
        try:
            # Проверка доступности слота
            if self._is_slot_occupied(booking.office_id, booking.scheduled_time):
                raise BookingConflictError("Time slot already occupied")

            db_booking = Booking.objects.create(
                user_id=booking.user_id,
                service_id=booking.service_id,
                office_id=booking.office_id,
                scheduled_time=booking.scheduled_time,
                status=booking.status.value,
                documents=booking.documents
            )
            return self._to_domain(db_booking)
        except Exception as e:
            logger.error(f"Booking creation error: {str(e)}")
            raise

    def get_available_slots(self, service_id: UUID, date: datetime) -> List[datetime]:
        # Логика расчета доступных слотов
        pass

    def cancel_booking(self, booking_id: UUID) -> None:
        try:
            booking = Booking.objects.get(id=booking_id)
            booking.status = 'canceled'
            booking.save()
        except Booking.DoesNotExist:
            raise BookingConflictError("Booking not found")

    def _is_slot_occupied(self, office_id: UUID, time: datetime) -> bool:
        return Booking.objects.filter(
            office_id=office_id,
            scheduled_time__range=(
                time - timedelta(minutes=29),
                time + timedelta(minutes=29)
            )
        ).exists()

    def _to_domain(self, db_booking: Booking) -> DomainBooking:
        return DomainBooking(
            id=db_booking.id,
            user_id=db_booking.user_id,
            service_id=db_booking.service_id,
            office_id=db_booking.office_id,
            scheduled_time=db_booking.scheduled_time,
            status=db_booking.status,
            documents=db_booking.documents,
            created_at=db_booking.created_at
        )
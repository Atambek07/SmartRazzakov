# modules/gov_connect/application/use_cases/service_booking.py
from datetime import datetime
from uuid import UUID
from ...domain.entities import BookingEntity
from ...domain.services import BookingService, QRService
from ...infrastructure.repositories import BookingRepository
from core.utils.responses import ResponseSuccess, ResponseFailure

class SlotAvailabilityUseCase:
    def __init__(self, repo: BookingRepository):
        self.repo = repo

    def get_available_slots(self, service_type: str, office_id: UUID, date: datetime):
        try:
            slots = self.repo.get_available_slots(service_type, office_id, date)
            return ResponseSuccess({
                "slots": [
                    {
                        "start": slot.start_time,
                        "end": slot.end_time,
                        "capacity": slot.available_capacity
                    } for slot in slots
                ]
            })
        except Exception as e:
            return ResponseFailure(f"Ошибка получения слотов: {str(e)}")

class BookingManagementUseCase:
    def __init__(
        self, 
        repo: BookingRepository,
        service: BookingService,
        qr: QRService
    ):
        self.repo = repo
        self.service = service
        self.qr = qr

    def create_booking(self, dto):
        try:
            # Проверка доступности
            if not self.service.check_availability(dto.office_id, dto.preferred_time):
                return ResponseFailure("Выбранное время недоступно")

            # Создание брони
            booking = BookingEntity(
                user_id=dto.user_id,
                service_type=dto.service_type,
                office_id=dto.office_id,
                scheduled_time=dto.preferred_time,
                documents=dto.documents
            )
            
            created = self.repo.create(booking)
            
            # Генерация QR
            qr_data = {
                "booking_id": str(created.id),
                "user_id": str(dto.user_id),
                "office_id": str(dto.office_id)
            }
            qr_url = self.qr.generate(qr_data)
            
            # Обновление записи
            updated = self.repo.add_qr_code(created.id, qr_url)
            
            return ResponseSuccess({
                "booking_id": str(updated.id),
                "qr_url": qr_url,
                "confirmation_code": updated.confirmation_code
            })
        except Exception as e:
            return ResponseFailure(f"Ошибка создания записи: {str(e)}")

    def cancel_booking(self, booking_id: UUID, user_id: UUID):
        try:
            booking = self.repo.get_by_user(booking_id, user_id)
            if not booking:
                return ResponseFailure("Запись не найдена")

            if booking.status != 'pending':
                return ResponseFailure("Невозможно отменить подтвержденную запись")

            self.repo.update_status(booking_id, 'canceled')
            return ResponseSuccess({"message": "Запись успешно отменена"})
        except Exception as e:
            return ResponseFailure(f"Ошибка отмены записи: {str(e)}")
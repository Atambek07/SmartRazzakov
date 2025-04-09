# modules/community_hub/domain/services/event_service.py
from datetime import datetime, timedelta
from typing import Optional
from uuid import UUID
from ...entities import CommunityEvent, EventStatus
from ...exceptions import (
    EventValidationError,
    BusinessRuleValidationError
)


class EventService:
    """Сервис для бизнес-логики мероприятий"""

    MIN_EVENT_DURATION = timedelta(minutes=30)
    MAX_EVENT_DURATION = timedelta(days=7)
    MAX_FUTURE_EVENTS = 50

    def validate_event_time(
            self,
            start_time: datetime,
            end_time: datetime,
            community_timezone: str = "UTC"
    ) -> bool:
        """Валидация времени мероприятия"""
        duration = end_time - start_time

        if start_time < datetime.utcnow():
            raise EventValidationError(
                field="start_time",
                reason="Event cannot start in the past"
            )

        if duration < self.MIN_EVENT_DURATION:
            raise EventValidationError(
                field="duration",
                reason=f"Event must last at least {self.MIN_EVENT_DURATION}"
            )

        if duration > self.MAX_EVENT_DURATION:
            raise EventValidationError(
                field="duration",
                reason=f"Event cannot last more than {self.MAX_EVENT_DURATION}"
            )

        return True

    def can_create_event(
            self,
            community_id: UUID,
            existing_events_count: int,
            user_role: Optional[str] = None
    ) -> bool:
        """Проверка возможности создания мероприятия"""
        if existing_events_count >= self.MAX_FUTURE_EVENTS:
            raise BusinessRuleValidationError(
                f"Cannot have more than {self.MAX_FUTURE_EVENTS} future events",
                code="event_limit_reached"
            )

        if user_role == "banned":
            raise PermissionDeniedError(
                action="create_event",
                reason="User is banned from creating events"
            )

        return True

    def update_event_status(
            self,
            event: CommunityEvent,
            new_status: EventStatus,
            updater_role: str
    ) -> CommunityEvent:
        """Обновление статуса мероприятия с проверкой прав"""
        status_transitions = {
            EventStatus.PLANNED: [EventStatus.ONGOING, EventStatus.CANCELLED],
            EventStatus.ONGOING: [EventStatus.COMPLETED]
        }

        allowed_roles = {
            EventStatus.CANCELLED: ["admin", "creator"],
            EventStatus.COMPLETED: ["admin", "creator", "organizer"]
        }

        if new_status not in status_transitions.get(event.status, []):
            raise BusinessRuleValidationError(
                f"Cannot transition from {event.status} to {new_status}",
                code="invalid_status_transition"
            )

        if new_status in allowed_roles and updater_role not in allowed_roles[new_status]:
            raise PermissionDeniedError(
                action=f"change_status_to_{new_status}",
                required_role=", ".join(allowed_roles[new_status])
            )

        event.status = new_status
        return event
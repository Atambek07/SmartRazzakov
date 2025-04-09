# modules/community_hub/application/use_cases/event_management.py
from datetime import datetime
from uuid import UUID
from typing import List
from ...domain.entities import CommunityEvent
from ....infrastructure.repositories import (
    EventRepository,
    MemberRepository
)
from ..dto import (
    EventCreateDTO,
    EventUpdateDTO,
    EventResponseDTO,
    EventListDTO
)
from . import CommunityBaseUseCase


class CreateEventUseCase(CommunityBaseUseCase[EventResponseDTO]):
    def __init__(
            self,
            event_repo: EventRepository,
            member_repo: MemberRepository
    ):
        self.event_repo = event_repo
        self.member_repo = member_repo

    async def execute(
            self,
            community_id: UUID,
            dto: EventCreateDTO,
            user_id: UUID
    ) -> EventResponseDTO:
        # Проверка прав пользователя
        if not await self.member_repo.is_member(user_id, community_id):
            raise PermissionDeniedException(
                "Only community members can create events"
            )

        new_event = CommunityEvent(
            id=await self.event_repo.generate_id(),
            community_id=community_id,
            title=dto.title,
            description=dto.description,
            organizer_id=user_id,
            start_time=dto.start_time,
            end_time=dto.end_time,
            location=dto.location,
            max_participants=dto.max_participants,
            is_online=dto.is_online,
            tags=dto.tags,
            status="planned",
            created_at=datetime.utcnow()
        )

        saved_event = await self.event_repo.save(new_event)
        return EventResponseDTO(**saved_event.dict())


class CancelEventUseCase(CommunityBaseUseCase[bool]):
    def __init__(
            self,
            event_repo: EventRepository,
            member_repo: MemberRepository
    ):
        self.event_repo = event_repo
        self.member_repo = member_repo

    async def execute(
            self,
            event_id: UUID,
            user_id: UUID
    ) -> bool:
        event = await self.event_repo.get_by_id(event_id)
        if not event:
            raise CommunityNotFoundException("Event not found")

        user_role = await self.member_repo.get_user_role(
            user_id, event.community_id
        )

        if user_role not in ["admin", "creator"] and user_id != event.organizer_id:
            raise PermissionDeniedException()

        event.status = "cancelled"
        await self.event_repo.save(event)
        return True
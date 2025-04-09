# modules/community_hub/infrastructure/repositories/event_repo.py
import logging
from typing import List, Optional
from uuid import UUID
from django.db import models, transaction
from django.utils import timezone
from ...models import CommunityEventModel, EventParticipation
from .. import BaseRepository
from domain.entities import CommunityEvent
from domain.exceptions import EventNotFoundError

logger = logging.getLogger(__name__)


class EventRepository(BaseRepository):
    """Реализация репозитория для работы с мероприятиями"""

    async def get_by_id(self, id: UUID) -> Optional[CommunityEvent]:
        try:
            event = await CommunityEventModel.objects.aget(id=id)
            return self._to_entity(event)
        except CommunityEventModel.DoesNotExist:
            raise EventNotFoundError(event_id=id)

    async def save(self, entity: CommunityEvent) -> CommunityEvent:
        try:
            async with transaction.atomic():
                if hasattr(entity, 'id') and entity.id:
                    event = await CommunityEventModel.objects.aget(id=entity.id)
                    for field, value in entity.dict().items():
                        setattr(event, field, value)
                    await event.asave()
                else:
                    event = await CommunityEventModel.objects.acreate(**self._to_model(entity))
                return self._to_entity(event)
        except Exception as e:
            logger.error(f"Error saving event: {str(e)}")
            raise

    async def delete(self, id: UUID) -> bool:
        try:
            event = await CommunityEventModel.objects.aget(id=id)
            await event.adelete()
            return True
        except CommunityEventModel.DoesNotExist:
            raise EventNotFoundError(event_id=id)

    async def get_upcoming_events(
            self,
            community_id: UUID,
            limit: int = 10
    ) -> List[CommunityEvent]:
        qs = CommunityEventModel.objects.filter(
            community_id=community_id,
            start_time__gte=timezone.now(),
            status='planned'
        ).order_by('start_time')[:limit]

        return [self._to_entity(event) async for event in qs]

    async def add_participant(
            self,
            event_id: UUID,
            user_id: UUID
    ) -> bool:
        try:
            await EventParticipation.objects.acreate(
                event_id=event_id,
                user_id=user_id
            )
            return True
        except Exception as e:
            logger.error(f"Error adding participant: {str(e)}")
            return False

    def _to_entity(self, model: CommunityEventModel) -> CommunityEvent:
        return CommunityEvent(
            id=model.id,
            community_id=model.community_id,
            title=model.title,
            description=model.description,
            organizer_id=model.organizer_id,
            start_time=model.start_time,
            end_time=model.end_time,
            location=model.location,
            status=model.status,
            max_participants=model.max_participants,
            is_online=model.is_online,
            created_at=model.created_at,
            updated_at=model.updated_at,
            tags=model.tags,
            cover_image_url=model.cover_image_url
        )

    def _to_model(self, entity: CommunityEvent) -> Dict:
        return {
            'id': entity.id,
            'community_id': entity.community_id,
            'title': entity.title,
            'description': entity.description,
            'organizer_id': entity.organizer_id,
            'start_time': entity.start_time,
            'end_time': entity.end_time,
            'location': entity.location,
            'status': entity.status,
            'max_participants': entity.max_participants,
            'is_online': entity.is_online,
            'tags': entity.tags,
            'cover_image_url': entity.cover_image_url
        }
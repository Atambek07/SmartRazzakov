# modules/community_hub/mappers.py
from typing import Dict, Any
from uuid import UUID
from datetime import datetime
from .domain.entities import (
    Community,
    CommunityMember,
    CommunityEvent,
    CommunityPost
)
from .infrastructure.models import (
    CommunityModel,
    CommunityMemberModel,
    CommunityEventModel,
    CommunityPostModel
)


class CommunityMapper:
    """Маппер для преобразования моделей сообществ"""

    @staticmethod
    def to_entity(model: CommunityModel) -> Community:
        """Преобразование модели Django в доменную сущность"""
        return Community(
            id=model.id,
            name=model.name,
            description=model.description,
            category=model.category,
            creator_id=model.creator_id,
            created_at=model.created_at,
            updated_at=model.updated_at,
            members_count=model.members_count,
            is_public=model.is_public,
            rules=model.rules,
            avatar_url=model.avatar_url,
            tags=model.tags,
            location=model.location,
            is_active=model.is_active
        )

    @staticmethod
    def to_model_data(entity: Community) -> Dict[str, Any]:
        """Преобразование доменной сущности в данные модели"""
        return {
            'id': entity.id,
            'name': entity.name,
            'description': entity.description,
            'category': entity.category,
            'creator_id': entity.creator_id,
            'members_count': entity.members_count,
            'is_public': entity.is_public,
            'rules': entity.rules,
            'avatar_url': entity.avatar_url,
            'tags': entity.tags,
            'location': entity.location,
            'is_active': entity.is_active
        }


class EventMapper:
    """Маппер для мероприятий"""

    @staticmethod
    def to_entity(model: CommunityEventModel) -> CommunityEvent:
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

    @staticmethod
    def to_model_data(entity: CommunityEvent) -> Dict[str, Any]:
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
# modules/community_hub/infrastructure/repositories/community_repo.py
import logging
from typing import List, Optional, Dict
from uuid import UUID
from django.db import transaction
from django.core.paginator import Paginator
from ...models import CommunityModel, CommunityMemberModel
from .. import BaseRepository
from domain.entities import Community, CommunityMember
from domain.exceptions import CommunityNotFoundError

logger = logging.getLogger(__name__)


class CommunityRepository(BaseRepository):
    """Реализация репозитория для работы с сообществами"""

    async def get_by_id(self, id: UUID) -> Optional[Community]:
        try:
            community = await CommunityModel.objects.aget(id=id)
            return self._to_entity(community)
        except CommunityModel.DoesNotExist:
            raise CommunityNotFoundError(community_id=id)

    async def save(self, entity: Community) -> Community:
        try:
            async with transaction.atomic():
                if hasattr(entity, 'id') and entity.id:
                    # Обновление существующего сообщества
                    community = await CommunityModel.objects.aget(id=entity.id)
                    for field, value in entity.dict().items():
                        setattr(community, field, value)
                    await community.asave()
                else:
                    # Создание нового сообщества
                    community = await CommunityModel.objects.acreate(**entity.dict())
                return self._to_entity(community)
        except Exception as e:
            logger.error(f"Error saving community: {str(e)}")
            raise

    async def delete(self, id: UUID) -> bool:
        try:
            community = await CommunityModel.objects.aget(id=id)
            await community.adelete()
            return True
        except CommunityModel.DoesNotExist:
            raise CommunityNotFoundError(community_id=id)

    async def search(
            self,
            query: Optional[str] = None,
            category: Optional[str] = None,
            tags: Optional[List[str]] = None,
            page: int = 1,
            page_size: int = 20
    ) -> Dict:
        """Поиск сообществ с пагинацией"""
        qs = CommunityModel.objects.all()

        if query:
            qs = qs.filter(
                models.Q(name__icontains=query) |
                models.Q(description__icontains=query)
            )

        if category:
            qs = qs.filter(category=category)

        if tags:
            qs = qs.filter(tags__overlap=tags)

        paginator = Paginator(qs, page_size)
        page_obj = await paginator.aget_page(page)

        return {
            'items': [self._to_entity(community) async for community in page_obj.object_list],
            'total': paginator.count,
            'page': page,
            'page_size': page_size
        }

    def _to_entity(self, model: CommunityModel) -> Community:
        """Конвертация модели Django в доменную сущность"""
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

    def _to_model(self, entity: Community) -> Dict:
        """Конвертация доменной сущности в словарь для модели Django"""
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
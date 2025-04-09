# modules/community_hub/infrastructure/repositories/member_repo.py
import logging
from typing import List, Optional
from uuid import UUID
from django.db import models, transaction
from ...models import CommunityMemberModel
from .. import BaseRepository
from domain.entities import CommunityMember
from domain.exceptions import MemberNotFoundError

logger = logging.getLogger(__name__)


class MemberRepository(BaseRepository):
    """Реализация репозитория для работы с участниками сообществ"""

    async def get_by_id(self, id: UUID) -> Optional[CommunityMember]:
        try:
            member = await CommunityMemberModel.objects.aget(id=id)
            return self._to_entity(member)
        except CommunityMemberModel.DoesNotExist:
            raise MemberNotFoundError(member_id=id)

    async def save(self, entity: CommunityMember) -> CommunityMember:
        try:
            async with transaction.atomic():
                if hasattr(entity, 'id') and entity.id:
                    member = await CommunityMemberModel.objects.aget(id=entity.id)
                    for field, value in entity.dict().items():
                        setattr(member, field, value)
                    await member.asave()
                else:
                    member = await CommunityMemberModel.objects.acreate(**self._to_model(entity))
                return self._to_entity(member)
        except Exception as e:
            logger.error(f"Error saving member: {str(e)}")
            raise

    async def delete(self, id: UUID) -> bool:
        try:
            member = await CommunityMemberModel.objects.aget(id=id)
            await member.adelete()
            return True
        except CommunityMemberModel.DoesNotExist:
            raise MemberNotFoundError(member_id=id)

    async def get_user_role(
            self,
            user_id: UUID,
            community_id: UUID
    ) -> Optional[str]:
        try:
            member = await CommunityMemberModel.objects.aget(
                user_id=user_id,
                community_id=community_id
            )
            return member.role
        except CommunityMemberModel.DoesNotExist:
            return None

    async def update_member_role(
            self,
            user_id: UUID,
            community_id: UUID,
            new_role: str
    ) -> bool:
        try:
            async with transaction.atomic():
                member = await CommunityMemberModel.objects.aget(
                    user_id=user_id,
                    community_id=community_id
                )
                member.role = new_role
                await member.asave()
                return True
        except CommunityMemberModel.DoesNotExist:
            raise MemberNotFoundError(
                user_id=user_id,
                community_id=community_id
            )

    def _to_entity(self, model: CommunityMemberModel) -> CommunityMember:
        return CommunityMember(
            id=model.id,
            user_id=model.user_id,
            community_id=model.community_id,
            role=model.role,
            contributions=model.contributions,
            joined_at=model.created_at,
            last_active=model.last_active,
            badges=model.badges
        )

    def _to_model(self, entity: CommunityMember) -> Dict:
        return {
            'user_id': entity.user_id,
            'community_id': entity.community_id,
            'role': entity.role,
            'contributions': entity.contributions,
            'last_active': entity.last_active,
            'badges': entity.badges
        }
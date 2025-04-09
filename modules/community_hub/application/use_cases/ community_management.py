# modules/community_hub/application/use_cases/community_management.py
import logging
from datetime import datetime
from uuid import UUID
from typing import List, Optional
from ...domain.entities import Community
from ...domain.services import CommunityService
from ....infrastructure.repositories import (
    CommunityRepository,
    MemberRepository
)
from ..dto import (
    CommunityCreateDTO,
    CommunityUpdateDTO,
    CommunityResponseDTO,
    CommunityListDTO
)
from . import CommunityBaseUseCase
from ....core.utils.auth import get_current_user

logger = logging.getLogger(__name__)


class CreateCommunityUseCase(CommunityBaseUseCase[CommunityResponseDTO]):
    def __init__(
            self,
            community_service: CommunityService,
            community_repo: CommunityRepository
    ):
        self.service = community_service
        self.repo = community_repo

    async def execute(self, dto: CommunityCreateDTO, user_id: UUID) -> CommunityResponseDTO:
        # Валидация бизнес-правил
        if not await self.service.is_valid_community_name(dto.name):
            raise ValidationException("Invalid community name")

        if await self.repo.exists_by_name(dto.name):
            raise ValidationException("Community with this name already exists")

        # Создание сущности
        new_community = Community(
            id=await self.repo.generate_id(),
            name=dto.name,
            description=dto.description,
            category=dto.category,
            creator_id=user_id,
            created_at=datetime.utcnow(),
            is_public=dto.is_public,
            rules=dto.rules,
            tags=dto.tags,
            location=dto.location
        )

        # Сохранение
        saved_community = await self.repo.save(new_community)

        # Добавление создателя как админа
        await MemberRepository().add_member(
            community_id=saved_community.id,
            user_id=user_id,
            role="creator"
        )

        logger.info(f"Community created: {saved_community.id}")
        return CommunityResponseDTO(**saved_community.dict())


class UpdateCommunityUseCase(CommunityBaseUseCase[CommunityResponseDTO]):
    def __init__(
            self,
            community_repo: CommunityRepository,
            member_repo: MemberRepository
    ):
        self.community_repo = community_repo
        self.member_repo = member_repo

    async def execute(
            self,
            community_id: UUID,
            dto: CommunityUpdateDTO,
            user_id: UUID
    ) -> CommunityResponseDTO:
        community = await self.community_repo.get_by_id(community_id)
        self._validate_community_exists(community)

        # Проверка прав
        user_role = await self.member_repo.get_user_role(user_id, community_id)
        if user_role not in ["admin", "creator"]:
            raise PermissionDeniedException()

        # Обновление полей
        update_data = dto.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(community, field, value)

        community.updated_at = datetime.utcnow()
        updated = await self.community_repo.save(community)
        return CommunityResponseDTO(**updated.dict())


class SearchCommunitiesUseCase(CommunityBaseUseCase[CommunityListDTO]):
    def __init__(self, community_repo: CommunityRepository):
        self.repo = community_repo

    async def execute(
            self,
            query: Optional[str] = None,
            category: Optional[str] = None,
            page: int = 1,
            per_page: int = 20
    ) -> CommunityListDTO:
        results, total = await self.repo.search(
            query=query,
            category=category,
            page=page,
            per_page=per_page
        )

        return CommunityListDTO(
            communities=[CommunityResponseDTO(**c.dict()) for c in results],
            total_count=total,
            page=page,
            per_page=per_page
        )
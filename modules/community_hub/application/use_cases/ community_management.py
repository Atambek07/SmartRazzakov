from ..domain.entities import Community, CommunityMember
from ..domain.services import CommunityManager
from .dto.community_dto import CreateCommunityDTO, AddMemberDTO


class CreateCommunityUseCase:
    def __init__(self, community_repository):
        self.repo = community_repository
        self.manager = CommunityManager()

    def execute(self, dto: CreateCommunityDTO) -> Community:
        """Создает новое сообщество и добавляет владельца"""
        community = Community(
            id=None,
            name=dto.name,
            description=dto.description,
            community_type=dto.community_type,
            members=[],
            created_at=datetime.now(),
            is_public=dto.is_public,
            rules=dto.rules
        )

        self.manager.add_member(community, dto.owner_id, MemberRole.OWNER)
        return self.repo.save(community)
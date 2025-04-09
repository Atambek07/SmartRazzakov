# modules/community_hub/application/use_cases/content_moderation.py
from uuid import UUID
from typing import Optional
from ...domain.entities import CommunityPost
from ....infrastructure.repositories import (
    PostRepository,
    MemberRepository,
    ReportRepository
)
from ..dto import ReportDTO
from . import CommunityBaseUseCase

class ModeratePostUseCase(CommunityBaseUseCase[bool]):
    def __init__(
        self,
        post_repo: PostRepository,
        member_repo: MemberRepository
    ):
        self.post_repo = post_repo
        self.member_repo = member_repo

    async def execute(
        self,
        post_id: UUID,
        action: str,  # 'approve'|'reject'|'delete'
        moderator_id: UUID,
        reason: Optional[str] = None
    ) -> bool:
        post = await self.post_repo.get_by_id(post_id)
        if not post:
            raise CommunityNotFoundException("Post not found")

        # Проверка прав модератора
        user_role = await self.member_repo.get_user_role(
            moderator_id, post.community_id
        )
        if user_role not in ["moderator", "admin", "creator"]:
            raise PermissionDeniedException()

        if action == "delete":
            await self.post_repo.delete(post_id)
        else:
            post.status = "approved" if action == "approve" else "rejected"
            post.moderator_id = moderator_id
            post.moderation_reason = reason
            await self.post_repo.save(post)

        return True

class CreateReportUseCase(CommunityBaseUseCase[ReportDTO]):
    def __init__(self, report_repo: ReportRepository):
        self.repo = report_repo

    async def execute(
        self,
        reporter_id: UUID,
        content_type: str,  # 'post'|'comment'|'event'
        content_id: UUID,
        reason: str
    ) -> ReportDTO:
        report = await self.repo.create(
            reporter_id=reporter_id,
            content_type=content_type,
            content_id=content_id,
            reason=reason
        )
        return ReportDTO(**report.dict())
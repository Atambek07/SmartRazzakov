from ..entities import Community, CommunityMember, MemberRole
from ..exceptions import CommunityException


class CommunityManager:
    def add_member(self, community: Community, user_id: str, role: MemberRole = MemberRole.MEMBER) -> None:
        """Добавляет участника в сообщество с проверкой правил"""
        if not community.is_public and role == MemberRole.MEMBER:
            raise CommunityException("Private communities require invitation")

        if any(m.user_id == user_id for m in community.members):
            raise CommunityException("User already in community")

        community.members.append(
            CommunityMember(
                user_id=user_id,
                role=role,
                joined_at=datetime.now()
            )
        )

    def promote_member(self, community: Community, target_user_id: str) -> None:
        """Повышает участника до модератора"""
        member = next((m for m in community.members if m.user_id == target_user_id), None)
        if not member:
            raise CommunityException("User not found in community")

        if member.role != MemberRole.MEMBER:
            raise CommunityException("Only regular members can be promoted")

        member.role = MemberRole.MODERATOR
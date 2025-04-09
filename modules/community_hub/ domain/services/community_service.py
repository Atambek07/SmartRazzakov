# modules/community_hub/domain/services/community_service.py
from datetime import datetime
from typing import Optional, List
from uuid import UUID
from ...entities import Community, CommunityMember, CommunityCategory
from ...exceptions import (
    BusinessRuleValidationError,
    PermissionDeniedError
)


class CommunityService:
    """Сервис для бизнес-логики работы с сообществами"""

    MAX_COMMUNITIES_PER_USER = 10
    MAX_TAGS_PER_COMMUNITY = 15
    MIN_DESCRIPTION_LENGTH = 10

    def validate_community_name(self, name: str) -> bool:
        """Валидация названия сообщества"""
        return (3 <= len(name) <= 100 and
                any(c.isalpha() for c in name) and
                not any(bad_word in name.lower()
                        for bad_word in ['admin', 'moder']))

    def can_user_create_community(self, user_id: UUID, existing_count: int) -> bool:
        """Может ли пользователь создать новое сообщество"""
        if existing_count >= self.MAX_COMMUNITIES_PER_USER:
            raise BusinessRuleValidationError(
                f"User cannot have more than {self.MAX_COMMUNITIES_PER_USER} communities",
                code="community_limit_reached"
            )
        return True

    def add_member_to_community(
            self,
            community: Community,
            member: CommunityMember,
            current_user_role: Optional[str] = None
    ) -> Community:
        """Добавление участника в сообщество с проверкой правил"""
        if not community.is_public and member.role == "member":
            if current_user_role not in ["admin", "creator"]:
                raise PermissionDeniedError(
                    "Only admins can add members to private communities"
                )

        if community.members_count >= getattr(community, 'max_members', 5000):
            raise BusinessRuleValidationError(
                "Community has reached maximum members limit",
                code="member_limit_reached"
            )

        community.members_count += 1
        return community

    def categorize_community(self, community: Community) -> str:
        """Автоматическая категоризация сообщества"""
        if not community.category:
            if any(tag in community.tags for tag in ['work', 'job']):
                return CommunityCategory.PROFESSIONAL
            elif any(tag in community.tags for tag in ['sport', 'hobby']):
                return CommunityCategory.HOBBY
        return community.category or CommunityCategory.NEIGHBORHOOD

    def update_community_stats(
            self,
            community: Community,
            new_members: int = 0,
            new_posts: int = 0,
            new_events: int = 0
    ) -> Community:
        """Обновление статистики сообщества"""
        community.members_count += new_members
        community.activity_score = (
                getattr(community, 'activity_score', 0) +
                new_posts * 0.5 +
                new_events * 0.8 +
                new_members * 0.3
        )
        community.last_activity = datetime.utcnow()
        return community
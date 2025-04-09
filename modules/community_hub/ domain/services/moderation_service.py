# modules/community_hub/domain/services/moderation_service.py
from datetime import datetime, timedelta
from typing import Optional
from uuid import UUID
from ...entities import CommunityPost
from ...exceptions import (
    ContentModerationError,
    PermissionDeniedError
)


class ModerationService:
    """Сервис для модерации контента и пользователей"""

    MAX_REPORTS_PER_USER = 5
    BAN_DURATION = timedelta(days=30)

    def moderate_post(
            self,
            post: CommunityPost,
            action: str,
            moderator_id: UUID,
            reason: Optional[str] = None,
            moderator_role: str = None
    ) -> CommunityPost:
        """Модерация публикации"""
        valid_actions = {
            "approve": "published",
            "reject": "rejected",
            "delete": "removed"
        }

        if action not in valid_actions:
            raise ContentModerationError(
                content_id=str(post.id),
                reason=f"Invalid action: {action}"
            )

        if moderator_role not in ["moderator", "admin", "creator"]:
            raise PermissionDeniedError(
                action="moderate_content",
                required_role="moderator"
            )

        if action == "delete":
            post.status = "removed"
        else:
            post.status = valid_actions[action]
            post.moderator_id = moderator_id
            post.moderation_reason = reason

        return post

    def evaluate_user_ban(
            self,
            user_id: UUID,
            reports_count: int,
            last_ban_date: Optional[datetime] = None
    ) -> Optional[timedelta]:
        """Определение необходимости бана пользователя"""
        if reports_count >= self.MAX_REPORTS_PER_USER:
            if last_ban_date and (datetime.utcnow() - last_ban_date) < self.BAN_DURATION * 2:
                return self.BAN_DURATION * 2  # Удвоенный бан за рецидив
            return self.BAN_DURATION
        return None

    def can_user_post(
            self,
            user_id: UUID,
            community_id: UUID,
            is_banned: bool,
            post_count: int,
            daily_limit: int = 10
    ) -> bool:
        """Проверка может ли пользователь публиковать контент"""
        if is_banned:
            raise PermissionDeniedError(
                action="create_post",
                reason="User is banned from posting"
            )

        if post_count >= daily_limit:
            raise BusinessRuleValidationError(
                f"Cannot post more than {daily_limit} times per day",
                code="post_limit_reached"
            )

        return True
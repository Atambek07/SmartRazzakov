# modules/community_hub/presentation/views/moderation_views.py
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from uuid import UUID
from ...application.use_cases import (
    ModeratePostUseCase,
    BanUserUseCase,
    HandleReportUseCase
)
from ..serializers import (
    MemberRoleSerializer
)
from . import BaseCommunityView
from core.permissions import IsCommunityModerator
from domain.exceptions import (
    PostNotFoundError,
    UserNotFoundError
)


class ModerationViewSet(BaseCommunityView, ViewSet):
    """ViewSet для модерации контента"""
    permission_classes = [IsAuthenticated, IsCommunityModerator]

    @action(detail=True, methods=['POST'])
    def moderate_post(self, request, pk=None) -> Response:
        """Модерация публикации"""
        try:
            post_id = self.validate_uuid(pk)
            action = request.data.get('action')
            reason = request.data.get('reason', '')

            use_case = ModeratePostUseCase()
            result = use_case.execute(
                post_id=post_id,
                action=action,
                moderator_id=request.user.id,
                reason=reason
            )

            return Response(
                {"status": "success", "new_status": result.status},
                status=status.HTTP_200_OK
            )
        except PostNotFoundError:
            return Response(
                {"error": "Post not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=True, methods=['POST'])
    def ban_user(self, request, pk=None) -> Response:
        """Блокировка пользователя в сообществе"""
        try:
            community_id = self.validate_uuid(pk)
            user_id = self.validate_uuid(request.data.get('user_id'))
            reason = request.data.get('reason', 'Violation of community rules')

            # use_case = BanUserUseCase()
            # await use_case.execute(
            #     community_id=community_id,
            #     user_id=user_id,
            #     moderator_id=request.user.id,
            #     reason=reason
            # )

            return Response(
                {"status": "user_banned"},
                status=status.HTTP_200_OK
            )
        except UserNotFoundError:
            return Response(
                {"error": "User not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
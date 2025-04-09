# modules/community_hub/presentation/views/__init__.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from typing import Any, Dict
from uuid import UUID
from core.permissions import IsAuthenticated, IsCommunityModerator
from ..exceptions import APIError

__all__ = [
    'CommunityViewSet',
    'CommunityMemberViewSet',
    'EventViewSet',
    'ModerationViewSet'
]


class BaseCommunityView(APIView):
    """Базовый view с общими методами"""
    permission_classes = [IsAuthenticated]

    def validate_uuid(self, uuid_str: str) -> UUID:
        """Валидация UUID с обработкой ошибок"""
        try:
            return UUID(uuid_str)
        except ValueError:
            raise APIError(
                "Invalid UUID format",
                code="invalid_uuid",
                status=status.HTTP_400_BAD_REQUEST
            )

    def handle_exception(self, exc):
        """Обработка исключений API"""
        if isinstance(exc, APIError):
            return Response(
                {"error": exc.message, "code": exc.code},
                status=exc.status
            )
        return super().handle_exception(exc)
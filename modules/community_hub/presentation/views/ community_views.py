# modules/community_hub/presentation/views/community_views.py
from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from uuid import UUID
from typing import List
from ...application.use_cases import (
    CreateCommunityUseCase,
    UpdateCommunityUseCase,
    SearchCommunitiesUseCase
)
from ..serializers import (
    CommunitySerializer,
    CommunityDetailSerializer,
    CommunityCreateSerializer
)
from . import BaseCommunityView
from domain.exceptions import (
    CommunityNotFoundError,
    PermissionDeniedError
)


class CommunityViewSet(BaseCommunityView, ViewSet):
    """ViewSet для работы с сообществами"""

    def list(self, request) -> Response:
        """Получение списка сообществ"""
        try:
            use_case = SearchCommunitiesUseCase()
            result = use_case.execute(
                query=request.query_params.get('q'),
                category=request.query_params.get('category'),
                page=int(request.query_params.get('page', 1)),
                per_page=int(request.query_params.get('per_page', 20))
            )

            serializer = CommunitySerializer(result.communities, many=True)
            return Response({
                'data': serializer.data,
                'meta': {
                    'total': result.total_count,
                    'page': result.page,
                    'per_page': result.per_page
                }
            })
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

    def retrieve(self, request, pk=None) -> Response:
        """Получение детальной информации о сообществе"""
        try:
            community_id = self.validate_uuid(pk)
            use_case = GetCommunityDetailsUseCase()
            community = use_case.execute(community_id)

            serializer = CommunityDetailSerializer(community)
            return Response(serializer.data)
        except CommunityNotFoundError:
            return Response(
                {"error": "Community not found"},
                status=status.HTTP_404_NOT_FOUND
            )

    def create(self, request) -> Response:
        """Создание нового сообщества"""
        serializer = CommunityCreateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            use_case = CreateCommunityUseCase()
            community = use_case.execute(
                serializer.validated_data,
                request.user.id
            )

            response_serializer = CommunityDetailSerializer(community)
            return Response(
                response_serializer.data,
                status=status.HTTP_201_CREATED
            )
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=True, methods=['POST'])
    def join(self, request, pk=None) -> Response:
        """Присоединение к сообществу"""
        try:
            community_id = self.validate_uuid(pk)
            use_case = JoinCommunityUseCase()
            membership = use_case.execute(community_id, request.user.id)

            return Response(
                {"status": "joined", "role": membership.role},
                status=status.HTTP_200_OK
            )
        except PermissionDeniedError as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_403_FORBIDDEN
            )
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
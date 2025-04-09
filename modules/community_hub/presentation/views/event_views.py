# modules/community_hub/presentation/views/event_views.py
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from uuid import UUID
from ...application.use_cases import (
    CreateEventUseCase,
    UpdateEventUseCase,
    CancelEventUseCase,
    GetEventDetailsUseCase
)
from ..serializers import (
    EventSerializer,
    EventCreateSerializer
)
from . import BaseCommunityView
from domain.exceptions import (
    EventNotFoundError,
    PermissionDeniedError
)


class EventViewSet(BaseCommunityView, ViewSet):
    """ViewSet для работы с мероприятиями"""

    def create(self, request, community_id=None) -> Response:
        """Создание нового мероприятия"""
        serializer = EventCreateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            community_id = self.validate_uuid(community_id)
            use_case = CreateEventUseCase()
            event = use_case.execute(
                community_id,
                serializer.validated_data,
                request.user.id
            )

            response_serializer = EventSerializer(event)
            return Response(
                response_serializer.data,
                status=status.HTTP_201_CREATED
            )
        except PermissionDeniedError:
            return Response(
                {"error": "Only community members can create events"},
                status=status.HTTP_403_FORBIDDEN
            )
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

    def retrieve(self, request, pk=None, community_id=None) -> Response:
        """Получение информации о мероприятии"""
        try:
            event_id = self.validate_uuid(pk)
            use_case = GetEventDetailsUseCase()
            event = use_case.execute(event_id)

            serializer = EventSerializer(event)
            return Response(serializer.data)
        except EventNotFoundError:
            return Response(
                {"error": "Event not found"},
                status=status.HTTP_404_NOT_FOUND
            )

    @action(detail=True, methods=['POST'])
    def register(self, request, pk=None, community_id=None) -> Response:
        """Регистрация на мероприятие"""
        try:
            event_id = self.validate_uuid(pk)
            use_case = RegisterForEventUseCase()
            await use_case.execute(event_id, request.user.id)

            return Response(
                {"status": "registered"},
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
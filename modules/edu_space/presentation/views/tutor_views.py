from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from ...application.dtos import TutorSearchDTO
from ...application.mappers import EduSpaceMapper
from ...domain.services import TutorService
from ...infrastructure.repositories import DjangoUserRepository
from ..serializers import (
    TutorProfileSerializer,
    TutorAvailabilitySerializer
)
from ..filters import TutorFilter
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class TutorViewSet(ReadOnlyModelViewSet):
    serializer_class = TutorProfileSerializer
    filterset_class = TutorFilter
    queryset = DjangoUserRepository().get_tutors()

    def get_queryset(self):
        """Расширенный поиск репетиторов"""
        queryset = super().get_queryset()
        params = self.request.query_params
        
        search_dto = TutorSearchDTO(
            subjects=params.getlist('subjects'),
            min_rating=float(params.get('min_rating', 4.0)),
            price_range=(
                float(params.get('min_price', 0)),
                float(params.get('max_price', 100000))
            ),
            availability=params.get('availability')
        )
        
        service = TutorService(DjangoUserRepository())
        return service.search_tutors(search_dto)

    @action(detail=True, methods=['get'])
    def schedule(self, request, pk=None):
        """Получение расписания репетитора"""
        try:
            from ...infrastructure.integrations import CalendarIntegration
            calendar = CalendarIntegration()
            
            tutor = self.get_object()
            schedule = calendar.get_schedule(
                user_id=tutor.id,
                start=request.query_params.get('start'),
                end=request.query_params.get('end')
            )
            
            return Response(schedule)
        
        except Exception as e:
            logger.error(f"Schedule fetch error: {str(e)}", exc_info=True)
            return Response(
                {'error': 'Unable to fetch schedule'}, 
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )

    @action(detail=True, methods=['post'])
    def book_session(self, request, pk=None):
        """Бронирование сессии с репетитором"""
        serializer = TutorAvailabilitySerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            from ...application.use_cases import BookingCoordinator
            coordinator = BookingCoordinator()
            
            booking = coordinator.create_booking(
                tutor_id=pk,
                student_id=request.user.id,
                start_time=serializer.validated_data['start_time'],
                duration=serializer.validated_data['duration']
            )
            
            return Response(
                {'booking_id': str(booking.id), 'meeting_link': booking.meeting_url},
                status=status.HTTP_201_CREATED
            )
        
        except Exception as e:
            return Response(
                {'error': str(e)}, 
                status=status.HTTP_400_BAD_REQUEST
            )
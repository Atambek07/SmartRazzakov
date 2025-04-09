from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status, permissions
from django.core.exceptions import PermissionDenied
from ...application.dtos import CourseCreateDTO, EnrollmentRequestDTO
from ...application.mappers import EduSpaceMapper
from ...domain.services import ClassroomService
from ...infrastructure.repositories import DjangoContentRepository
from ..serializers import (
    CourseSerializer,
    EnrollmentRequestSerializer,
    LiveSessionSerializer
)
import logging

logger = logging.getLogger(__name__)

class CourseViewSet(ModelViewSet):
    serializer_class = CourseSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = DjangoContentRepository().list_courses()

    def get_queryset(self):
        """Фильтрация курсов с расширенными параметрами"""
        queryset = super().get_queryset()
        params = self.request.query_params
        
        # Фильтры
        if subject := params.get('subject'):
            queryset = queryset.filter(subject__iexact=subject)
        if level := params.get('level'):
            queryset = queryset.filter(level=level.upper())
        if min_price := params.get('min_price'):
            queryset = queryset.filter(price__gte=min_price)
        
        return queryset.select_related('tutor').prefetch_related('enrolled_students')

    def perform_create(self, serializer):
        """Создание курса с валидацией прав"""
        if not self.request.user.has_perm('edu_space.add_course'):
            logger.warning(f"Unauthorized course creation attempt by {self.request.user}")
            raise PermissionDenied("You don't have permission to create courses")
        
        dto = CourseCreateDTO(**serializer.validated_data)
        service = ClassroomService(DjangoContentRepository())
        course = service.create_course(dto, self.request.user.id)
        serializer.instance = course

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def enroll(self, request, pk=None):
        """Запись студента на курс с обработкой платежей"""
        serializer = EnrollmentRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            enrollment_dto = EnrollmentRequestDTO(
                course_id=pk,
                student_id=serializer.validated_data['student_id'],
                payment_token=serializer.validated_data.get('payment_token')
            )
            
            service = ClassroomService(DjangoContentRepository())
            result = service.process_enrollment(enrollment_dto)
            
            return Response({
                'status': 'success',
                'payment_status': result.payment_status,
                'next_steps': result.next_steps
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            logger.error(f"Enrollment error: {str(e)}", exc_info=True)
            return Response(
                {'error': str(e)}, 
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=True, methods=['post'], url_path='schedule-session')
    def schedule_session(self, request, pk=None):
        """Создание сессии видеоконференции для курса"""
        course = self.get_object()
        serializer = LiveSessionSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            from ...infrastructure.integrations import VideoServiceFactory
            video_service = VideoServiceFactory.get_service()
            
            meeting = video_service.create_meeting(
                title=f"{course.title} Session",
                start_time=serializer.validated_data['start_time'],
                duration=serializer.validated_data['duration'],
                password=serializer.validated_data.get('password')
            )
            
            course.metadata['meetings'] = course.metadata.get('meetings', []) + [meeting]
            course.save()
            
            return Response(meeting, status=status.HTTP_201_CREATED)
        
        except Exception as e:
            return Response(
                {'error': f"Video service error: {str(e)}"},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )
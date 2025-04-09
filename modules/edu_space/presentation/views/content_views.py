from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status, parsers
from ...application.dtos import ContentUploadDTO, ContentSearchDTO
from ...application.mappers import EduSpaceMapper
from ...domain.services import ContentService
from ...infrastructure.repositories import DjangoContentRepository
from ..serializers import (
    EducationalContentSerializer,
    InteractiveTestSerializer
)
from ..permissions import IsContentAuthorOrReadOnly
import uuid
import logging

logger = logging.getLogger(__name__)

class ContentViewSet(ModelViewSet):
    serializer_class = EducationalContentSerializer
    permission_classes = [IsContentAuthorOrReadOnly]
    parser_classes = [parsers.MultiPartParser, parsers.JSONParser]
    queryset = DjangoContentRepository().list_content()

    def get_queryset(self):
        """Расширенный поиск контента"""
        queryset = super().get_queryset()
        params = self.request.query_params
        
        search_dto = ContentSearchDTO(
            query=params.get('q'),
            subjects=params.getlist('subject'),
            types=params.getlist('type'),
            grade_level=params.get('grade'),
            min_rating=params.get('min_rating', 4.0)
        )
        
        service = ContentService(DjangoContentRepository())
        return service.search_content(search_dto)

    @action(detail=True, methods=['post'], parser_classes=[parsers.MultiPartParser])
    def upload_file(self, request, pk=None):
        """Загрузка файла контента с обработкой разных форматов"""
        try:
            content = self.get_object()
            file = request.FILES['file']
            
            from ...infrastructure.storage import MediaStorage
            storage = MediaStorage()
            file_url = storage.upload(
                file=file,
                directory=f"content/{content.id}",
                allowed_types=['pdf', 'mp4', 'zip']
            )
            
            content.file_url = file_url
            content.save()
            
            return Response(
                {'file_url': file_url}, 
                status=status.HTTP_201_CREATED
            )
        
        except Exception as e:
            logger.error(f"File upload error: {str(e)}", exc_info=True)
            return Response(
                {'error': str(e)}, 
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=True, methods=['post'])
    def publish(self, request, pk=None):
        """Публикация контента с проверкой готовности"""
        content = self.get_object()
        
        try:
            service = ContentService(DjangoContentRepository())
            published_content = service.publish_content(content.id)
            
            return Response(
                self.serializer_class(published_content).data,
                status=status.HTTP_200_OK
            )
        
        except Exception as e:
            return Response(
                {'error': str(e)}, 
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=True, methods=['post'])
    def generate_test(self, request, pk=None):
        """Генерация интерактивного теста"""
        serializer = InteractiveTestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            service = ContentService(DjangoContentRepository())
            test_session = service.generate_test_session(
                content_id=pk,
                config=serializer.validated_data
            )
            
            return Response(test_session, status=status.HTTP_201_CREATED)
        
        except Exception as e:
            return Response(
                {'error': str(e)}, 
                status=status.HTTP_422_UNPROCESSABLE_ENTITY
            )
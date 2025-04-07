from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from application.use_cases import (
    GetTaleContentUseCase,
    UpdateUserPreferenceUseCase
)
from infrastructure.repositories import (
    TaleRepository,
    UserPreferencesRepository
)
from domain.services import ContentFormatService
from .serializers import (
    TaleContentSerializer,
    QRRequestSerializer,
    UserPreferenceSerializer
)
import logging

logger = logging.getLogger(__name__)

class TaleContentView(APIView):
    """
    API для получения контента по QR-коду.
    Поддерживает JWT-аутентификацию через заголовок Authorization.
    """
    
    def get_use_case(self) -> GetTaleContentUseCase:
        return GetTaleContentUseCase(
            tale_repo=TaleRepository(),
            prefs_repo=UserPreferencesRepository(),
            format_service=ContentFormatService()
        )

    @extend_schema(
        request=QRRequestSerializer,
        responses={200: TaleContentSerializer}
    )
    def post(self, request):
        serializer = QRRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            use_case = self.get_use_case()
            tale_content = use_case.execute(serializer.validated_data)
            return Response(
                TaleContentSerializer(tale_content).data,
                status=status.HTTP_200_OK
            )
        except Exception as e:
            logger.error(f"Ошибка при обработке QR: {str(e)}")
            return Response(
                {"error": str(e)},
                status=status.HTTP_404_NOT_FOUND if "не найден" in str(e) 
                else status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class UserPreferenceView(APIView):
    """API для управления предпочтениями формата."""
    
    @extend_schema(
        request=UserPreferenceSerializer,
        responses={204: None}
    )
    def patch(self, request):
        serializer = UserPreferenceSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            use_case = UpdateUserPreferenceUseCase(
                prefs_repo=UserPreferencesRepository()
            )
            use_case.execute(serializer.validated_data)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            logger.error(f"Ошибка обновления предпочтений: {str(e)}")
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
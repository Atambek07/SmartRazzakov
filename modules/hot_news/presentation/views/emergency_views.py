from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema
from core.api import (
    JWTAuthentication,
    EmergencyAccessPermission,
    handle_exceptions
)
from modules.hot_news.application.use_cases import EmergencyAlertUseCase

class EmergencyAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [EmergencyAccessPermission]

    @extend_schema(
        request=EmergencyAlertSerializer,
        responses={201: NewsResponseSerializer}
    )
    @handle_exceptions
    def post(self, request):
        """Создание экстренного оповещения"""
        serializer = EmergencyAlertSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        use_case = EmergencyAlertUseCase()
        result = use_case.create_emergency(
            serializer.validated_data,
            request.user.id
        )
        
        return Response(
            NewsResponseSerializer(result).data,
            status=status.HTTP_201_CREATED
        )
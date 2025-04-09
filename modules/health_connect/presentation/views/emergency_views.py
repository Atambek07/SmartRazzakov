# modules/health_connect/presentation/views/emergency_views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from ...application.use_cases import (
    TriggerEmergencyUseCase,
    FindEmergencyProvidersUseCase
)
from ..serializers import EmergencyAlertSerializer

class EmergencyRequestAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        serializer = EmergencyAlertSerializer(data=request.data)
        if serializer.is_valid():
            use_case = TriggerEmergencyUseCase()
            result = use_case.execute(
                serializer.validated_data, 
                request.user
            )
            if result.is_success:
                return Response(result.data, status=status.HTTP_202_ACCEPTED)
            return Response(result.error, status=result.status_code)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EmergencyProvidersAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        use_case = FindEmergencyProvidersUseCase()
        result = use_case.execute(request.user.location)
        return Response(result.data)
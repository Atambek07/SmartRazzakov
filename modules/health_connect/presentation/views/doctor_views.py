# modules/health_connect/presentation/views/doctor_views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsDoctor
from ...application.use_cases import (
    ConfirmAppointmentUseCase,
    GetDoctorScheduleUseCase
)
from ..serializers import AppointmentResponseSerializer

class DoctorScheduleAPIView(APIView):
    permission_classes = [IsAuthenticated, IsDoctor]
    
    def get(self, request):
        use_case = GetDoctorScheduleUseCase()
        result = use_case.execute(request.user.doctor_profile)
        serializer = AppointmentResponseSerializer(result.data, many=True)
        return Response(serializer.data)

class ConfirmAppointmentAPIView(APIView):
    permission_classes = [IsAuthenticated, IsDoctor]
    
    def post(self, request, appointment_id):
        use_case = ConfirmAppointmentUseCase()
        result = use_case.execute(appointment_id)
        if result.is_success:
            serializer = AppointmentResponseSerializer(result.data)
            return Response(serializer.data)
        return Response(result.error, status=result.status_code)
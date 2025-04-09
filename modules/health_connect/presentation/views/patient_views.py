# modules/health_connect/presentation/views/patient_views.py
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from core.utils.permissions import IsPatient
from ...application.use_cases import (
    GetMedicalRecordsUseCase,
    CreateAppointmentUseCase,
    CancelAppointmentUseCase
)
from ..serializers import (
    MedicalRecordResponseSerializer,
    AppointmentCreateSerializer,
    AppointmentResponseSerializer
)

class MedicalRecordViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated, IsPatient]
    
    def list(self, request):
        use_case = GetMedicalRecordsUseCase()
        result = use_case.execute(request.user.patient_profile)
        serializer = MedicalRecordResponseSerializer(result.data, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        use_case = GetMedicalRecordUseCase()
        result = use_case.execute(pk, request.user)
        if result.is_success:
            serializer = MedicalRecordResponseSerializer(result.data)
            return Response(serializer.data)
        return Response(result.error, status=status.HTTP_404_NOT_FOUND)

class PatientAppointmentViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated, IsPatient]
    
    def create(self, request):
        serializer = AppointmentCreateSerializer(data=request.data)
        if serializer.is_valid():
            use_case = CreateAppointmentUseCase()
            result = use_case.execute(serializer.validated_data)
            if result.is_success:
                return Response(
                    AppointmentResponseSerializer(result.data).data,
                    status=status.HTTP_201_CREATED
                )
            return Response(result.error, status=result.status_code)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        use_case = CancelAppointmentUseCase()
        result = use_case.execute(pk, request.user)
        if result.is_success:
            return Response({'status': 'appointment cancelled'})
        return Response(result.error, status=result.status_code)
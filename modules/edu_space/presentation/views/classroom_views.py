from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..application.use_cases.classroom_operations import ScheduleClassUseCase
from ..infrastructure.repositories import DjangoClassroomRepository
from ..domain.services import ClassroomService

class ClassroomScheduleView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ClassroomScheduleSerializer(data=request.data)
        if serializer.is_valid():
            service = ClassroomService(DjangoClassroomRepository())
            use_case = ScheduleClassUseCase(service)
            classroom = use_case.execute(serializer.validated_data)
            return Response(classroom.to_dict(), status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
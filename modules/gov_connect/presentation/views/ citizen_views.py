from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..application.use_cases import SubmitComplaintUseCase
from ..domain.services import ComplaintWorkflow
from ..infrastructure.repositories import DjangoComplaintRepository

class CitizenComplaintAPI(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = CitizenComplaintSerializer(data=request.data)
        if serializer.is_valid():
            use_case = SubmitComplaintUseCase(
                repository=DjangoComplaintRepository(),
                workflow_engine=ComplaintWorkflow()
            )
            complaint = use_case.execute(serializer.validated_data)
            return Response(
                CitizenComplaintSerializer(complaint).data,
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .application.use_cases import CreateStoryUseCase
from .infrastructure.repositories import DjangoStoryRepository
from .serializers import StorySerializer

class StoryCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = StorySerializer(data=request.data)
        if serializer.is_valid():
            use_case = CreateStoryUseCase(DjangoStoryRepository())
            result = use_case.execute(serializer.validated_data)
            return Response(result, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
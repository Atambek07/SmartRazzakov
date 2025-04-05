from rest_framework.views import APIView
from rest_framework.response import Response
from ..application.use_cases import CreateCommunityUseCase
from ..infrastructure.repositories import DjangoCommunityRepository

class CommunityAPI(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = CommunitySerializer(data=request.data)
        if serializer.is_valid():
            use_case = CreateCommunityUseCase(DjangoCommunityRepository())
            community = use_case.execute(serializer.validated_data)
            return Response(
                CommunitySerializer(community).data,
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
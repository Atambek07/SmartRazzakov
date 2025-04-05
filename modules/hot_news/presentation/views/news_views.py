from rest_framework.views import APIView
from rest_framework.response import Response
from ..application.use_cases import CreateNewsUseCase
from ..infrastructure.repositories import DjangoNewsRepository
from ..domain.services import NewsValidator

class NewsAPI(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def post(self, request):
        serializer = NewsSerializer(data=request.data)
        if serializer.is_valid():
            use_case = CreateNewsUseCase(
                repository=DjangoNewsRepository(),
                news_validator=NewsValidator()
            )
            news_item = use_case.execute(serializer.validated_data)
            return Response(NewsSerializer(news_item).data, status=201)
        return Response(serializer.errors, status=400)
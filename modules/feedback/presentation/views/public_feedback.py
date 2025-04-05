from rest_framework.views import APIView
from rest_framework.response import Response
from ..application.use_cases import SubmitReviewUseCase
from ..infrastructure.repositories import DjangoReviewRepository
from ..domain.services import RatingCalculator

class PublicReviewAPI(APIView):
    def post(self, request):
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            use_case = SubmitReviewUseCase(
                repository=DjangoReviewRepository(),
                rating_calculator=RatingCalculator()
            )
            result = use_case.execute(serializer.validated_data)
            return Response(result, status=201)
        return Response(serializer.errors, status=400)
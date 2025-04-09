# modules/feedback/presentation/views/public_views.py
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from ...application.use_cases import (
    CreateReviewUseCase,
    GetReviewUseCase,
    CalculateRatingUseCase
)
from ...infrastructure.repositories import DjangoReviewRepository
from ..serializers import (
    ReviewCreateSerializer,
    ReviewResponseSerializer,
    RatingSummarySerializer,
    ReviewFilterSerializer
)
from core.api.permissions import IsOwnerOrReadOnly

class ReviewListCreateView(generics.ListCreateAPIView):
    serializer_class = ReviewResponseSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_serializer = ReviewFilterSerializer

    def get_queryset(self):
        queryset = DjangoReviewRepository().query().approved()
        filter_serializer = self.filter_serializer(data=self.request.query_params)
        filter_serializer.is_valid(raise_exception=True)
        
        return queryset.filter(
            rating__gte=filter_serializer.validated_data.get('min_rating', 1),
            content_type=filter_serializer.validated_data.get('content_type'),
            images__isnull=not filter_serializer.validated_data.get('has_media', False)
        ).distinct()

    def post(self, request, *args, **kwargs):
        serializer = ReviewCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        use_case = CreateReviewUseCase(
            repo=DjangoReviewRepository(),
            rating_calculator=CalculateRatingUseCase()
        )
        review = use_case.execute(serializer.save())
        
        return Response(
            ReviewResponseSerializer(review).data,
            status=status.HTTP_201_CREATED
        )

class ReviewDetailView(generics.RetrieveAPIView):
    queryset = DjangoReviewRepository().query().with_relations()
    serializer_class = ReviewResponseSerializer
    permission_classes = [IsOwnerOrReadOnly]
    lookup_field = 'id'

class RatingSummaryView(generics.RetrieveAPIView):
    serializer_class = RatingSummarySerializer

    def get_object(self):
        content_ref = ContentRefDTO(
            content_type=self.kwargs['content_type'],
            object_id=self.kwargs['object_id'],
            module=self.kwargs['module']
        )
        return CalculateRatingUseCase().execute(content_ref)

class ReviewVoteView(generics.CreateAPIView):
    serializer_class = ReviewVoteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        review = DjangoReviewRepository().get_by_id(self.kwargs['review_id'])
        serializer.save(user=self.request.user, review=review)
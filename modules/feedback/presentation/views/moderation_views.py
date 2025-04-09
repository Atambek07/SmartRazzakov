# modules/feedback/presentation/views/moderation_views.py
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from ...application.use_cases import ModerateReviewUseCase
from ...infrastructure.integrations import get_default_moderator
from ..serializers import ReviewResponseSerializer

class ModerationQueueView(generics.ListAPIView):
    serializer_class = ReviewResponseSerializer
    permission_classes = [permissions.IsAdminUser]

    def get_queryset(self):
        return DjangoReviewRepository().query().filter(
            status=Review.ReviewStatus.PENDING
        )

class ModerationActionView(generics.UpdateAPIView):
    serializer_class = ReviewResponseSerializer
    permission_classes = [permissions.IsAdminUser]

    def update(self, request, *args, **kwargs):
        use_case = ModerateReviewUseCase(
            repo=DjangoReviewRepository(),
            moderation_api=get_default_moderator()
        )
        review = use_case.execute(kwargs['review_id'])
        return Response(self.get_serializer(review).data)
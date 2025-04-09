# modules/feedback/infrastructure/repositories/rating_repo.py
from django.db.models import Count, Avg
from django.contrib.contenttypes.models import ContentType
from ...domain.entities import RatingSummary
from ...models import RatingSnapshot, Review
from ...application.dto import ContentRefDTO

class RatingQuerySet:
    def __init__(self, queryset):
        self.queryset = queryset
    
    def for_period(self, start_date, end_date):
        return self.queryset.filter(
            created_at__gte=start_date,
            created_at__lte=end_date
        )
    
    def group_by_module(self):
        return self.queryset.values('source_module').annotate(
            avg_rating=Avg('rating'),
            total=Count('id')
        )

class DjangoRatingRepository:
    def __init__(self):
        self.model = RatingSnapshot
        self.review_model = Review

    def _to_entity(self, snapshot) -> RatingSummary:
        return RatingSummary(
            content_type=snapshot.content_type.model,
            object_id=snapshot.object_id,
            average_rating=float(snapshot.average_rating),
            total_reviews=snapshot.total_reviews,
            rating_distribution=snapshot.rating_distribution,
            calculated_at=snapshot.calculated_at,
            confidence_score=snapshot.confidence_score
        )

    def get_ratings(self, content_ref: ContentRefDTO) -> RatingSummary:
        # Получение актуального снимка
        try:
            snapshot = self.model.objects.filter(
                content_type=ContentType.objects.get(
                    app_label=content_ref.module,
                    model=content_ref.content_type
                ),
                object_id=content_ref.object_id
            ).latest('calculated_at')
            return self._to_entity(snapshot)
        except self.model.DoesNotExist:
            return self._calculate_current_rating(content_ref)

    def _calculate_current_rating(self, content_ref: ContentRefDTO) -> RatingSummary:
        # Агрегация данных в реальном времени
        reviews = self.review_model.objects.filter(
            content_type=ContentType.objects.get(
                app_label=content_ref.module,
                model=content_ref.content_type
            ),
            object_id=content_ref.object_id,
            status=Review.ReviewStatus.APPROVED
        )
        
        rating_distribution = reviews.values('rating').annotate(count=Count('id'))
        dist_dict = {item['rating']: item['count'] for item in rating_distribution}
        
        avg_rating = reviews.aggregate(avg=Avg('rating'))['avg'] or 0.0
        
        return RatingSummary(
            content_type=content_ref.content_type,
            object_id=content_ref.object_id,
            average_rating=round(avg_rating, 2),
            total_reviews=reviews.count(),
            rating_distribution=dist_dict,
            calculated_at=timezone.now()
        )

    def create_snapshot(self, content_ref: ContentRefDTO):
        current = self._calculate_current_rating(content_ref)
        return self.model.objects.create(
            content_type=ContentType.objects.get(
                app_label=content_ref.module,
                model=content_ref.content_type
            ),
            object_id=content_ref.object_id,
            average_rating=current.average_rating,
            total_reviews=current.total_reviews,
            rating_distribution=current.rating_distribution,
            source_module=content_ref.module
        )

    def query(self) -> RatingQuerySet:
        return RatingQuerySet(self.model.objects.all())
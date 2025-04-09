# modules/feedback/infrastructure/repositories/review_repo.py
from django.db.models import Q, Count, Avg
from django.contrib.contenttypes.models import ContentType
from ...domain.entities import ReviewEntity
from ...application.dto import ContentRefDTO
from ...models import Review, ReviewImage, ReviewTag
from core.exceptions import NotFoundException

class ReviewQuerySet:
    def __init__(self, queryset):
        self.queryset = queryset
    
    def filter_by_type(self, content_ref: ContentRefDTO):
        return self.queryset.filter(
            content_type=ContentType.objects.get(
                app_label=content_ref.module,
                model=content_ref.content_type
            ),
            object_id=content_ref.object_id
        )
    
    def with_relations(self):
        return self.queryset.select_related(
            'author'
        ).prefetch_related(
            'images',
            'tags'
        )
    
    def approved(self):
        return self.queryset.filter(status=Review.ReviewStatus.APPROVED)

class DjangoReviewRepository:
    def __init__(self):
        self.model = Review
        self.image_model = ReviewImage
        self.tag_model = ReviewTag

    def _to_entity(self, review) -> ReviewEntity:
        return ReviewEntity(
            id=review.id,
            author_id=review.author_id,
            content_type=review.content_type.model,
            object_id=review.object_id,
            rating=review.rating,
            text=review.text,
            media={
                'audio': review.audio.url if review.audio else None,
                'video': review.video.url if review.video else None,
                'images': [img.image.url for img in review.images.all()]
            },
            tags=list(review.tags.values_list('name', flat=True)),
            status=review.status,
            created_at=review.created_at,
            updated_at=review.updated_at,
            source_module=review.source_module,
            helpful_count=review.helpful_count,
            reply_count=review.reply_count
        )

    def get_by_id(self, review_id: int) -> ReviewEntity:
        try:
            review = self.model.objects.with_relations().get(pk=review_id)
            return self._to_entity(review)
        except self.model.DoesNotExist:
            raise NotFoundException("Review not found")

    def create(self, dto) -> ReviewEntity:
        content_type = ContentType.objects.get(
            app_label=dto.source_module,
            model=dto.content_type
        )
        
        review = self.model.objects.create(
            author_id=dto.author_id,
            content_type=content_type,
            object_id=dto.object_id,
            rating=dto.rating,
            text=dto.text,
            audio=dto.media.get('audio'),
            video=dto.media.get('video'),
            status=dto.status,
            source_module=dto.source_module
        )
        
        # Добавление изображений
        for image in dto.media.get('images', []):
            ReviewImage.objects.create(review=review, image=image)
        
        # Добавление тегов
        tags = self.tag_model.objects.filter(name__in=dto.tags)
        review.tags.set(tags)
        
        return self._to_entity(review)

    def update(self, review_id: int, dto) -> ReviewEntity:
        review = self.model.objects.get(pk=review_id)
        
        for field, value in dto.dict(exclude_unset=True).items():
            if field == 'media':
                self._update_media(review, value)
            elif field == 'tags':
                tags = self.tag_model.objects.filter(name__in=value)
                review.tags.set(tags)
            else:
                setattr(review, field, value)
        
        review.save()
        return self._to_entity(review)

    def _update_media(self, review, media_data):
        if 'audio' in media_data:
            review.audio = media_data['audio']
        if 'video' in media_data:
            review.video = media_data['video']
        if 'images' in media_data:
            review.images.all().delete()
            for image in media_data['images']:
                ReviewImage.objects.create(review=review, image=image)

    def check_existing_review(self, author_id: int, content_ref: ContentRefDTO) -> bool:
        return self.model.objects.filter(
            author_id=author_id,
            content_type=ContentType.objects.get(
                app_label=content_ref.module,
                model=content_ref.content_type
            ),
            object_id=content_ref.object_id
        ).exists()

    def query(self) -> ReviewQuerySet:
        return ReviewQuerySet(self.model.objects.all())
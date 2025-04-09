# modules/feedback/mappers.py
from datetime import datetime
from typing import Optional
from .domain.entities import ReviewEntity, RatingSummary
from .application.dto import ReviewResponseDTO, RatingSummaryDTO
from .models import Review, RatingSnapshot

class ReviewMapper:
    @staticmethod
    def to_dto(entity: ReviewEntity) -> ReviewResponseDTO:
        return ReviewResponseDTO(
            id=entity.id,
            author_id=entity.author_id,
            content_type=entity.content_type,
            object_id=entity.object_id,
            rating=entity.rating,
            text=entity.text,
            media=entity.media,
            tags=entity.tags,
            status=entity.status,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
            source_module=entity.source_module,
            helpful_count=entity.helpful_count,
            reply_count=entity.reply_count
        )

    @staticmethod
    def to_entity(model: Review) -> ReviewEntity:
        return ReviewEntity(
            id=model.id,
            author_id=model.author_id,
            content_type=model.content_type.model,
            object_id=model.object_id,
            rating=model.rating,
            text=model.text,
            media={
                'audio': model.audio.url if model.audio else None,
                'video': model.video.url if model.video else None,
                'images': [img.image.url for img in model.images.all()]
            },
            tags=list(model.tags.values_list('name', flat=True)),
            status=model.status,
            created_at=model.created_at,
            updated_at=model.updated_at,
            source_module=model.source_module,
            helpful_count=model.helpful_count,
            reply_count=model.reply_count
        )

class RatingMapper:
    @staticmethod
    def to_dto(entity: RatingSummary) -> RatingSummaryDTO:
        return RatingSummaryDTO(
            total_reviews=entity.total_reviews,
            average_rating=entity.average_rating,
            rating_distribution=entity.rating_distribution,
            compared_to_similar=entity.confidence_score
        )

    @staticmethod
    def from_snapshot(model: RatingSnapshot) -> RatingSummary:
        return RatingSummary(
            content_type=model.content_type.model,
            object_id=model.object_id,
            average_rating=float(model.average_rating),
            total_reviews=model.total_reviews,
            rating_distribution=model.rating_distribution,
            calculated_at=model.calculated_at,
            confidence_score=model.confidence_score
        )
from datetime import datetime
from typing import List, Optional, Dict, Any
from ...domain.entities import (
    NewsArticle, 
    NewsCategory,
    NewsPriority,
    NewsSubscription
)
from ..dto import (
    NewsCreateDTO,
    NewsUpdateDTO,
    NewsResponseDTO,
    SubscriptionCreateDTO,
    SubscriptionResponseDTO
)
from modules.hot_news.infrastructure.models import (
    NewsArticleModel,
    NewsSubscriptionModel
)
from core.utils.mapping import BaseMapper, Converter

class NewsMapper(BaseMapper):
    @staticmethod
    def dto_to_entity(dto: NewsCreateDTO | NewsUpdateDTO) -> NewsArticle:
        return NewsArticle(
            title=dto.title,
            content=dto.content,
            category=Converter.enum_to_str(dto.category),
            priority=Converter.enum_to_int(dto.priority),
            geo_location=dto.geo_location,
            sources=dto.sources,
            media_attachments=dto.media_attachments,
            sentiment_score=0.0,
            created_at=datetime.now(),
            modified_at=datetime.now()
        )

    @staticmethod
    def entity_to_dto(entity: NewsArticle) -> NewsResponseDTO:
        return NewsResponseDTO(
            id=str(entity.id),
            title=entity.title,
            content=entity.content,
            category=Converter.str_to_enum(entity.category, NewsCategory),
            priority=Converter.int_to_enum(entity.priority, NewsPriority),
            geo_location=entity.geo_location,
            sources=entity.sources,
            media_attachments=entity.media_attachments,
            created_at=entity.created_at,
            modified_at=entity.modified_at,
            views_count=entity.views_count,
            is_published=entity.is_published,
            author_id=entity.author_id,
            publish_at=entity.publish_at
        )

    @staticmethod
    def model_to_entity(model: NewsArticleModel) -> NewsArticle:
        return NewsArticle(
            id=str(model.id),
            title=model.title,
            content=model.content,
            category=model.category,
            priority=model.priority,
            geo_location=model.geo_location,
            sources=model.sources,
            media_attachments=model.media_attachments,
            sentiment_score=model.sentiment_score,
            created_at=model.created_at,
            modified_at=model.modified_at,
            views_count=model.views_count,
            is_published=model.is_published,
            author_id=model.author_id,
            publish_at=model.publish_at
        )

    @staticmethod
    def entity_to_model(entity: NewsArticle) -> Dict[str, Any]:
        return {
            'title': entity.title,
            'content': entity.content,
            'category': entity.category,
            'priority': entity.priority,
            'geo_location': entity.geo_location,
            'sources': entity.sources,
            'media_attachments': entity.media_attachments,
            'sentiment_score': entity.sentiment_score,
            'views_count': entity.views_count,
            'is_published': entity.is_published,
            'author_id': entity.author_id,
            'publish_at': entity.publish_at
        }

class SubscriptionMapper(BaseMapper):
    @staticmethod
    def dto_to_entity(dto: SubscriptionCreateDTO) -> NewsSubscription:
        return NewsSubscription(
            user_id=dto.user_id,
            categories=[Converter.enum_to_str(c) for c in dto.categories],
            notification_channels={
                'email': dto.notify_by_email,
                'push': dto.notify_by_push,
                'sms': dto.notify_by_sms
            },
            preferred_language=dto.preferred_language,
            created_at=datetime.now(),
            is_active=True
        )

    @staticmethod
    def entity_to_dto(entity: NewsSubscription) -> SubscriptionResponseDTO:
        return SubscriptionResponseDTO(
            id=str(entity.id),
            user_id=entity.user_id,
            categories=[Converter.str_to_enum(c, NewsCategory) for c in entity.categories],
            notify_by_email=entity.notification_channels.get('email', False),
            notify_by_push=entity.notification_channels.get('push', True),
            notify_by_sms=entity.notification_channels.get('sms', False),
            preferred_language=entity.preferred_language,
            created_at=entity.created_at,
            is_active=entity.is_active
        )

    @staticmethod
    def model_to_entity(model: NewsSubscriptionModel) -> NewsSubscription:
        return NewsSubscription(
            id=str(model.id),
            user_id=model.user_id,
            categories=model.categories,
            notification_channels=model.notification_channels,
            preferred_language=model.preferred_language,
            created_at=model.created_at,
            is_active=model.is_active
        )

    @staticmethod
    def entity_to_model(entity: NewsSubscription) -> Dict[str, Any]:
        return {
            'user_id': entity.user_id,
            'categories': entity.categories,
            'notification_channels': entity.notification_channels,
            'preferred_language': entity.preferred_language,
            'is_active': entity.is_active
        }

class EmergencyAlertMapper:
    @staticmethod
    def gov_report_to_news(gov_report: Dict) -> NewsArticle:
        return NewsArticle(
            title=gov_report.get('title'),
            content=gov_report.get('summary'),
            category=NewsCategory.GOVERNMENT,
            priority=NewsPriority.HIGH,
            geo_location=gov_report.get('location'),
            sources=[gov_report.get('source_url')],
            is_published=False,
            author_id='gov-connect-system'
        )

    @staticmethod
    def community_event_to_news(event: Dict) -> NewsArticle:
        return NewsArticle(
            title=f"Новое событие: {event.get('title')}",
            content=event.get('description'),
            category=NewsCategory.COMMUNITY,
            priority=NewsPriority.NORMAL,
            geo_location=event.get('location'),
            sources=[f"/community/events/{event.get('id')}"],
            media_attachments=event.get('images', []),
            is_published=True,
            author_id=event.get('organizer_id')
        )

__all__ = ['NewsMapper', 'SubscriptionMapper', 'EmergencyAlertMapper']
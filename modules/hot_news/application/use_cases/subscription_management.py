from typing import List, Optional
from abc import ABC, abstractmethod
from ...domain.entities import NewsCategory, NewsSubscription
from ...domain.services import SubscriptionService
from ..dto.subscription_dto import SubscriptionCreateDTO, SubscriptionUpdateDTO, SubscriptionResponseDTO
from core.utils.responses import ResponseSuccess, ResponseFailure
from modules.notification.domain.services import NotificationService
from modules.user_management.domain.models import UserPreferences

class SubscriptionManagementUseCase:
    def __init__(
        self,
        subscription_service: SubscriptionService,
        notification_service: NotificationService
    ):
        self.subscription_service = subscription_service
        self.notification_service = notification_service

    async def create_subscription(self, dto: SubscriptionCreateDTO) -> ResponseSuccess:
        try:
            subscription = NewsSubscription(
                user_id=dto.user_id,
                categories=dto.categories,
                notification_channels=self._get_channels(dto),
                preferred_language=dto.preferred_language
            )
            
            result = await self.subscription_service.create(subscription)
            
            # Обновление пользовательских предпочтений
            await UserPreferences.update_notification_settings(
                user_id=dto.user_id,
                settings={
                    'news_categories': dto.categories,
                    'notification_prefs': {
                        'email': dto.notify_by_email,
                        'push': dto.notify_by_push,
                        'sms': dto.notify_by_sms
                    }
                }
            )
            
            return ResponseSuccess(result.to_dto(SubscriptionResponseDTO))
        
        except Exception as e:
            return ResponseFailure(str(e))

    async def update_subscription(self, subscription_id: str, dto: SubscriptionUpdateDTO) -> ResponseSuccess:
        try:
            subscription = await self.subscription_service.get_by_id(subscription_id)
            if not subscription:
                raise SubscriptionNotFoundError()
            
            update_data = dto.dict(exclude_unset=True)
            if 'categories' in update_data:
                subscription.categories = update_data['categories']
            if 'preferred_language' in update_data:
                subscription.preferred_language = update_data['preferred_language']
            
            subscription.notification_channels = self._get_channels(dto)
            
            result = await self.subscription_service.update(subscription_id, subscription)
            return ResponseSuccess(result.to_dto(SubscriptionResponseDTO))
        
        except Exception as e:
            return ResponseFailure(str(e))

    async def send_notifications(self, article: NewsArticle):
        subscribers = await self.subscription_service.get_subscribers_for_category(article.category)
        
        for subscriber in subscribers:
            localized_content = self._localize_content(
                article.content,
                subscriber.preferred_language
            )
            
            await self.notification_service.send(
                user_id=subscriber.user_id,
                message={
                    'title': article.title,
                    'content': localized_content,
                    'category': article.category,
                    'priority': article.priority
                },
                channels=subscriber.notification_channels
            )

    def _get_channels(self, dto) -> List[str]:
        channels = []
        if dto.notify_by_email:
            channels.append('email')
        if dto.notify_by_push:
            channels.append('push')
        if dto.notify_by_sms:
            channels.append('sms')
        return channels

    def _localize_content(self, content: str, lang: str) -> str:
        # Интеграция с сервисом перевода
        return TranslationService.translate(content, lang)
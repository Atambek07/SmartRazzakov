from uuid import UUID
from typing import List, Optional
from django.db import transaction
from modules.hot_news.domain.entities import NewsSubscription, NewsCategory
from modules.hot_news.infrastructure.models.subscriptions import NewsSubscriptionModel
from modules.hot_news.application.mappers import SubscriptionMapper

class SubscriptionRepository:
    def __init__(self):
        self.mapper = SubscriptionMapper()

    @transaction.atomic
    async def create(self, entity: NewsSubscription) -> NewsSubscription:
        existing = NewsSubscriptionModel.objects.filter(user_id=entity.user_id).first()
        if existing:
            return self.mapper.model_to_entity(existing)
            
        data = self.mapper.entity_to_model(entity)
        model = NewsSubscriptionModel.objects.create(**data)
        return self.mapper.model_to_entity(model)

    async def get_by_id(self, subscription_id: str) -> Optional[NewsSubscription]:
        try:
            model = NewsSubscriptionModel.objects.get(pk=UUID(subscription_id))
            return self.mapper.model_to_entity(model)
        except NewsSubscriptionModel.DoesNotExist:
            return None

    @transaction.atomic
    async def update(self, subscription_id: str, entity: NewsSubscription) -> NewsSubscription:
        model = NewsSubscriptionModel.objects.select_for_update().get(pk=UUID(subscription_id))
        update_data = self.mapper.entity_to_model(entity)
        
        for field, value in update_data.items():
            setattr(model, field, value)
        
        model.save(update_fields=update_data.keys())
        return self.mapper.model_to_entity(model)

    async def get_subscribers_for_category(self, category: NewsCategory) -> List[NewsSubscription]:
        queryset = NewsSubscriptionModel.objects.filter(
            categories__contains=[category.value],
            is_active=True
        )
        return [self.mapper.model_to_entity(sub) for sub in queryset]
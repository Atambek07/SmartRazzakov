from django.core.paginator import Paginator
from django.db import transaction
from django.db.models import Q, F
from uuid import UUID
from typing import Optional, List, Dict
from core.utils.pagination import PaginationParams, PaginatedResults
from modules.hot_news.domain.entities import NewsArticle
from modules.hot_news.infrastructure.models.news import NewsArticleModel
from modules.hot_news.application.mappers import NewsMapper

class NewsRepository:
    def __init__(self):
        self.mapper = NewsMapper()

    @transaction.atomic
    async def create(self, entity: NewsArticle) -> NewsArticle:
        try:
            data = self.mapper.entity_to_model(entity)
            model = NewsArticleModel.objects.create(**data)
            return self.mapper.model_to_entity(model)
        except IntegrityError as e:
            raise NewsValidationError(f"Duplicate article: {str(e)}")

    async def get_by_id(self, article_id: str) -> Optional[NewsArticle]:
        try:
            model = NewsArticleModel.objects.get(pk=UUID(article_id))
            return self.mapper.model_to_entity(model)
        except NewsArticleModel.DoesNotExist:
            return None

    @transaction.atomic
    async def update(self, article_id: str, entity: NewsArticle) -> NewsArticle:
        model = NewsArticleModel.objects.select_for_update().get(pk=UUID(article_id))
        update_data = self.mapper.entity_to_model(entity)
        
        for field, value in update_data.items():
            setattr(model, field, value)
        
        model.save(update_fields=update_data.keys())
        return self.mapper.model_to_entity(model)

    async def delete(self, article_id: str) -> bool:
        deleted, _ = NewsArticleModel.objects.filter(pk=UUID(article_id)).delete()
        return deleted > 0

    async def list_all(
        self,
        pagination: PaginationParams,
        filters: Dict[str, any] = None
    ) -> PaginatedResults[NewsArticle]:
        queryset = NewsArticleModel.objects.all().order_by('-created_at')
        
        if filters:
            q_objects = Q()
            for field, value in filters.items():
                if field == 'category':
                    q_objects &= Q(category=value)
                elif field == 'priority':
                    q_objects &= Q(priority=value)
                elif field == 'author_id':
                    q_objects &= Q(author_id=UUID(value))
            queryset = queryset.filter(q_objects)
        
        paginator = Paginator(queryset, pagination.page_size)
        page = paginator.get_page(pagination.page_number)
        
        return PaginatedResults(
            items=[self.mapper.model_to_entity(item) for item in page.object_list],
            total=page.paginator.count,
            page=pagination.page_number,
            page_size=pagination.page_size
        )

    async def increment_views(self, article_id: str) -> int:
        return NewsArticleModel.objects.filter(pk=UUID(article_id)).update(
            views_count=F('views_count') + 1
        )
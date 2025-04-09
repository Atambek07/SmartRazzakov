from abc import ABC, abstractmethod
from typing import Optional, List, Dict
from ...domain.entities import NewsArticle, NewsPriority, NewsCategory
from core.utils.pagination import PaginationParams, PaginatedResults

class NewsService(ABC):
    @abstractmethod
    async def create(self, article: NewsArticle) -> NewsArticle:
        pass

    @abstractmethod
    async def get_by_id(self, article_id: str) -> Optional[NewsArticle]:
        pass

    @abstractmethod
    async def update(self, article_id: str, article: NewsArticle) -> NewsArticle:
        pass

    @abstractmethod
    async def delete(self, article_id: str) -> bool:
        pass

    @abstractmethod
    async def list_all(
        self, 
        pagination: PaginationParams,
        filters: Dict[str, any] = None
    ) -> PaginatedResults[NewsArticle]:
        pass

    @abstractmethod
    async def publish(self, article_id: str) -> NewsArticle:
        pass

    @abstractmethod
    async def increment_views(self, article_id: str) -> int:
        pass

    @abstractmethod
    async def search(
        self,
        query: str,
        category: Optional[NewsCategory] = None,
        priority: Optional[NewsPriority] = None
    ) -> List[NewsArticle]:
        pass
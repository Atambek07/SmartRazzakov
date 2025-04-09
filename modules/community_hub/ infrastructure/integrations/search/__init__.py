# modules/community_hub/infrastructure/integrations/search/__init__.py
from abc import ABC, abstractmethod
from typing import List, Dict, Optional, Any
from uuid import UUID
from dataclasses import dataclass
from pydantic import BaseModel


class SearchError(Exception):
    """Базовое исключение для поисковых операций"""
    pass


@dataclass
class SearchResult:
    """Результат поиска"""
    items: List[Dict[str, Any]]
    total: int
    facets: Dict[str, Dict[str, int]]


class BaseSearchClient(ABC):
    """Абстрактный клиент поиска"""

    @abstractmethod
    async def index_document(self, index: str, doc_id: str, document: Dict) -> bool:
        """Индексация документа"""
        pass

    @abstractmethod
    async def search(
            self,
            index: str,
            query: str,
            filters: Optional[Dict] = None,
            facets: Optional[List[str]] = None,
            page: int = 1,
            size: int = 20
    ) -> SearchResult:
        """Поиск документов"""
        pass

    @abstractmethod
    async def delete_document(self, index: str, doc_id: str) -> bool:
        """Удаление документа из индекса"""
        pass

    @abstractmethod
    async def update_document(
            self,
            index: str,
            doc_id: str,
            partial_update: Dict
    ) -> bool:
        """Частичное обновление документа"""
        pass


class TagEngine(ABC):
    """Абстрактный движок для работы с тегами"""

    @abstractmethod
    async def extract_tags(self, text: str) -> List[str]:
        """Извлечение тегов из текста"""
        pass

    @abstractmethod
    async def suggest_tags(self, prefix: str) -> List[str]:
        """Подсказки тегов по префиксу"""
        pass

    @abstractmethod
    async def related_tags(self, tags: List[str]) -> Dict[str, List[str]]:
        """Поиск связанных тегов"""
        pass


__all__ = [
    'BaseSearchClient',
    'TagEngine',
    'SearchError',
    'SearchResult'
]
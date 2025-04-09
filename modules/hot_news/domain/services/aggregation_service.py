from abc import ABC, abstractmethod
from typing import List
from ...domain.entities import NewsArticle
from modules.gov_connect.domain.dtos import GovReportDTO
from modules.community_hub.domain.entities import CommunityEvent
from core.utils.mapping import Mapper

class AggregationService(ABC):
    @abstractmethod
    async def fetch_gov_reports(self) -> List[GovReportDTO]:
        pass

    @abstractmethod
    async def fetch_community_events(self) -> List[CommunityEvent]:
        pass

    @abstractmethod
    async def fetch_external_news(self, sources: List[str]) -> List[dict]:
        pass

    @abstractmethod
    async def aggregate_news(
        self,
        internal_news: List[NewsArticle],
        external_news: List[dict]
    ) -> List[NewsArticle]:
        """Агрегирует и ранжирует новости по бизнес-правилам"""
        pass

    @abstractmethod
    async def process_rss_feeds(self, rss_urls: List[str]) -> List[NewsArticle]:
        pass

class DefaultNewsAggregator(AggregationService):
    def __init__(self, gov_adapter, community_adapter, rss_parser):
        self.gov_adapter = gov_adapter
        self.community_adapter = community_adapter
        self.rss_parser = rss_parser

    async def aggregate_news(self, internal, external):
        # Приоритизация: экстренные > правительственные > другие
        prioritized = sorted(
            internal + external,
            key=lambda x: (
                x.priority.value if isinstance(x, NewsArticle) else 0,
                x.created_at if hasattr(x, 'created_at') else datetime.min
            ),
            reverse=True
        )
        return prioritized[:100]  # Лимит на выдачу
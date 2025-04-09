from typing import Dict, List
from dataclasses import dataclass
from aiohttp import ClientSession
from aiocache import cached, Cache
from .rss_parser import RSSParser
from modules.hot_news.domain.entities import NewsArticle
from core.utils.mapping import Converter

@dataclass
class RSSSource:
    url: str
    category: str
    priority: int
    enabled: bool = True
    last_fetch: Optional[datetime] = None

class RSSFeedManager:
    def __init__(self, sources: List[RSSSource]):
        self.sources = {source.url: source for source in sources}
        self.parser = RSSParser()
        self.http_session = ClientSession()

    async def refresh_all_feeds(self):
        """Обновление всех активных RSS-лент"""
        tasks = [
            self.update_feed(source.url)
            for source in self.sources.values()
            if source.enabled
        ]
        await asyncio.gather(*tasks)

    async def update_feed(self, url: str):
        """Обновление конкретной ленты и сохранение в кэш"""
        if url not in self.sources:
            raise ValueError(f"Unknown RSS source: {url}")
        
        try:
            items = await self.parser.parse_feed(url)
            await self._process_items(items, url)
            self.sources[url].last_fetch = datetime.now()
        except Exception as e:
            logger.error(f"Failed to update {url}: {str(e)}")

    async def _process_items(self, items: List[RSSItem], url: str):
        """Конвертация RSSItem в NewsArticle"""
        source = self.sources[url]
        for item in items:
            article = NewsArticle(
                title=item.title,
                content=item.summary,
                category=Converter.str_to_enum(
                    item.category, 
                    NewsCategory,
                    default=NewsCategory.OTHER
                ),
                priority=source.priority,
                sources=[url],
                media_attachments=[],
                author_id=f"rss:{source.url}",
                geo_location=None,
                is_published=True
            )
            await self._save_article(article)

    async def _save_article(self, article: NewsArticle):
        """Интеграция с NewsService"""
        from modules.hot_news.domain.services import NewsService
        service = NewsService()
        if not await service.exists(article.title, article.sources[0]):
            await service.create(article)

    async def add_source(self, source: RSSSource):
        """Добавление нового источника"""
        self.sources[source.url] = source
        await self.update_feed(source.url)

    async def disable_source(self, url: str):
        """Отключение источника"""
        if url in self.sources:
            self.sources[url].enabled = False

    async def get_articles(
        self, 
        url: str, 
        limit: int = 20
    ) -> List[NewsArticle]:
        """Получение статей из конкретного RSS-источника"""
        items = await self.parser.parse_feed(url)
        return items[:limit]
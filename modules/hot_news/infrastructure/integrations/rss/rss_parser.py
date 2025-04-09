import asyncio
import feedparser
from datetime import datetime
from typing import List, Dict, Optional
from pydantic import BaseModel, ValidationError
from aiocache import cached, Cache
from aiocache.serializers import JsonSerializer
from core.utils.logging import get_logger
from modules.hot_news.domain.entities import NewsArticle, NewsCategory

logger = get_logger(__name__)

class RSSItem(BaseModel):
    title: str
    link: str
    published: datetime
    summary: str
    author: Optional[str]
    category: Optional[str]

class RSSParser:
    def __init__(self, timeout: int = 10, max_entries: int = 50):
        self.timeout = timeout
        self.max_entries = max_entries

    async def parse_feed(self, url: str) -> List[RSSItem]:
        """Асинхронный парсинг RSS-ленты с кэшированием"""
        try:
            return await self._fetch_and_parse(url)
        except Exception as e:
            logger.error(f"RSS parse error for {url}: {str(e)}")
            return []

    @cached(
        ttl=300, 
        cache=Cache.REDIS,
        key_builder=lambda f, *args, **kwargs: f"rss:{args[1]}",
        serializer=JsonSerializer()
    )
    async def _fetch_and_parse(self, url: str) -> List[RSSItem]:
        """Основная логика парсинга с обработкой в отдельном потоке"""
        loop = asyncio.get_event_loop()
        feed = await loop.run_in_executor(
            None, 
            lambda: feedparser.parse(
                url,
                etag=None,
                modified=None,
                agent='SmartRazzakov/1.0',
                timeout=self.timeout
            )
        )
        
        if feed.bozo:
            raise ValueError(f"Invalid RSS feed: {feed.bozo_exception}")

        return self._normalize_feed(feed)

    def _normalize_feed(self, feed) -> List[RSSItem]:
        """Нормализация данных из разных форматов RSS"""
        items = []
        for entry in feed.entries[:self.max_entries]:
            try:
                pub_date = self._parse_date(
                    entry.get('published_parsed') or 
                    entry.get('updated_parsed')
                )
                
                items.append(RSSItem(
                    title=entry.title,
                    link=entry.link,
                    published=pub_date,
                    summary=entry.get('summary', ''),
                    author=entry.get('author'),
                    category=entry.get('tags', [{}])[0].get('term', 'general')
                ))
            except (KeyError, ValidationError) as e:
                logger.warning(f"Invalid RSS entry: {str(e)}")
        return items

    def _parse_date(self, time_tuple: Optional[tuple]) -> datetime:
        """Конвертация разных форматов дат"""
        if time_tuple:
            return datetime.fromtimestamp(mktime(time_tuple))
        return datetime.now()
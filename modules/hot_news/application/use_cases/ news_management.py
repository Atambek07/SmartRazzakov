from datetime import datetime
from typing import Optional, List
from abc import ABC, abstractmethod
from ...domain.entities import NewsArticle, NewsPriority, NewsCategory
from ...domain.services import NewsService, NewsValidator
from ...domain.exceptions import NewsValidationError, NewsNotFoundError
from ..dto.news_dto import NewsCreateDTO, NewsUpdateDTO, NewsResponseDTO
from core.utils.responses import ResponseSuccess, ResponseFailure
from modules.feedback.application.use_cases import SentimentAnalysisUseCase
from modules.gov_connect.domain.services import GovReportService

class NewsManagementUseCase:
    def __init__(
        self,
        news_service: NewsService,
        validator: NewsValidator,
        gov_integration: GovReportService,
        sentiment_analyzer: SentimentAnalysisUseCase
    ):
        self.news_service = news_service
        self.validator = validator
        self.gov_integration = gov_integration
        self.sentiment_analyzer = sentiment_analyzer

    async def create_article(self, dto: NewsCreateDTO, author_id: str) -> ResponseSuccess:
        try:
            # Интеграция с GovConnect для верификации официальных отчетов
            if NewsCategory.GOVERNMENT in dto.category:
                await self.gov_integration.verify_official_report(dto.sources[0])
            
            # Анализ тональности контента
            sentiment = await self.sentiment_analyzer.analyze(dto.content)
            if sentiment.score < -0.5:
                raise NewsValidationError("Content contains negative sentiment")
            
            entity = NewsArticle(
                title=dto.title,
                content=dto.content,
                category=dto.category,
                priority=dto.priority,
                geo_location=dto.geo_location,
                sources=dto.sources,
                media_attachments=dto.media_attachments,
                author_id=author_id,
                sentiment_score=sentiment.score
            )
            
            self.validator.validate(entity)
            result = await self.news_service.create(entity)
            return ResponseSuccess(result.to_dto(NewsResponseDTO))
        
        except Exception as e:
            return ResponseFailure(str(e))

    async def update_article(self, article_id: str, dto: NewsUpdateDTO) -> ResponseSuccess:
        try:
            article = await self.news_service.get_by_id(article_id)
            if not article:
                raise NewsNotFoundError()
            
            update_data = dto.dict(exclude_unset=True)
            updated_article = article.copy(update=update_data)
            
            self.validator.validate(updated_article)
            result = await self.news_service.update(article_id, updated_article)
            return ResponseSuccess(result.to_dto(NewsResponseDTO))
        
        except Exception as e:
            return ResponseFailure(str(e))

    async def publish_article(self, article_id: str) -> ResponseSuccess:
        try:
            article = await self.news_service.get_by_id(article_id)
            if not article:
                raise NewsNotFoundError()
            
            article.is_published = True
            article.publish_at = datetime.now()
            
            result = await self.news_service.update(article_id, article)
            
            # Интеграция с CommunityHub для анонсов
            if article.category == NewsCategory.COMMUNITY:
                await CommunityHubIntegration.announce_event(
                    title=article.title,
                    content=article.content[:100] + "...",
                    link=f"/news/{article_id}"
                )
            
            return ResponseSuccess(result.to_dto(NewsResponseDTO))
        
        except Exception as e:
            return ResponseFailure(str(e))

    async def delete_article(self, article_id: str) -> ResponseSuccess:
        try:
            await self.news_service.delete(article_id)
            return ResponseSuccess({"status": "deleted"})
        except Exception as e:
            return ResponseFailure(str(e))
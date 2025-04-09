# modules/feedback/domain/services/review_service.py
from ...domain.entities import ReviewEntity
from .sentiment_analysis import BaseSentimentAnalyzer
import re

class ReviewValidator:
    def __init__(self, analyzer: BaseSentimentAnalyzer):
        self.analyzer = analyzer
        self.banned_phrases = [
            r'\b(спам|реклама|обман)\b',
            r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
        ]

    def validate_content(self, review: ReviewEntity) -> dict:
        """Проверка содержания отзыва"""
        errors = []
        
        # Проверка текста
        if review.text:
            # Проверка на запрещенные фразы
            for pattern in self.banned_phrases:
                if re.search(pattern, review.text, re.IGNORECASE):
                    errors.append('contains_banned_content')
            
            # Анализ тональности
            sentiment = self.analyzer.analyze(review.text)
            if sentiment['score'] < -0.5:
                errors.append('negative_sentiment')
        
        # Проверка медиа-контента
        if review.media:
            if len(review.media.images) > 5:
                errors.append('too_many_images')
            
            if review.media.video_url and not review.text:
                errors.append('video_without_text')
        
        return {
            'is_valid': len(errors) == 0,
            'errors': errors,
            'sentiment': sentiment
        }

class ReviewModerator:
    def __init__(self, validator: ReviewValidator):
        self.validator = validator

    def moderate(self, review: ReviewEntity) -> dict:
        """Автоматическая модерация отзыва"""
        validation = self.validator.validate_content(review)
        
        decision = {
            'status': 'pending',
            'flags': [],
            'score': 0
        }

        if validation['is_valid']:
            decision['status'] = 'approved' 
            if validation['sentiment']['score'] > 0.7:
                decision['flags'].append('highlight')
        else:
            decision['status'] = 'needs_review'
            decision['flags'] = validation['errors']

        return decision
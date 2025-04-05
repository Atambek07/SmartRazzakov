from ..entities import NewsItem, NewsPriority
from ..exceptions import NewsValidationError

class NewsValidator:
    @staticmethod
    def validate_news(news_data: dict) -> None:
        """Проверяет обязательные поля новости"""
        required_fields = ['title', 'content', 'category']
        for field in required_fields:
            if not news_data.get(field):
                raise NewsValidationError(f"Missing required field: {field}")

    @staticmethod
    def determine_priority(news_data: dict) -> NewsPriority:
        """Определяет приоритет новости"""
        if news_data.get('category') == 'emergency':
            return NewsPriority.CRITICAL
        elif 'важно' in news_data.get('title', '').lower():
            return NewsPriority.HIGH
        return NewsPriority.MEDIUM
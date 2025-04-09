# modules/feedback/domain/services/rating_service.py
from dataclasses import dataclass
from ...domain.entities import RatingSummary
from datetime import datetime, timedelta

@dataclass
class RatingConfig:
    recent_days: int = 30
    verified_bonus: float = 0.2
    min_reviews: int = 5

class RatingCalculator:
    def __init__(self, config: RatingConfig = RatingConfig()):
        self.config = config

    def calculate_weighted_rating(self, reviews: list) -> RatingSummary:
        """Рассчитывает рейтинг с учетом весовых коэффициентов"""
        if not reviews:
            return RatingSummary(0, 0.0, {})

        total = len(reviews)
        weighted_sum = 0.0
        distribution = {1:0, 2:0, 3:0, 4:0, 5:0}
        time_now = datetime.now()

        for review in reviews:
            # Вес отзыва в зависимости от давности
            days_old = (time_now - review.created_at).days
            time_weight = max(0, 1 - days_old/self.config.recent_days)
            
            # Бонус за проверенные отзывы
            verified_weight = self.config.verified_bonus if review.is_verified else 0
            
            total_weight = 1.0 + time_weight + verified_weight
            weighted_sum += review.rating * total_weight
            distribution[review.rating] += 1

        average = weighted_sum / (total * (1 + self.config.verified_bonus))
        return RatingSummary(
            total_reviews=total,
            average_rating=round(average, 1),
            rating_distribution=distribution
        )

    def calculate_bayesian_estimate(self, reviews: list) -> float:
        """Байесовская оценка для объектов с малым числом отзывов"""
        C = 3.0  # Средний рейтинг по системе
        m = self.config.min_reviews
        
        if len(reviews) < m:
            summary = self.calculate_weighted_rating(reviews)
            return (summary.total_reviews * summary.average_rating + C * m) / (summary.total_reviews + m)
        return self.calculate_weighted_rating(reviews).average_rating
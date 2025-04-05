from ..entities import Review
from ..exceptions import RatingValidationError


class RatingCalculator:
    @staticmethod
    def calculate_average(reviews: list[Review]) -> float:
        """Вычисляет средний рейтинг с проверкой валидности"""
        if not reviews:
            return 0.0

        valid_reviews = [r for r in reviews if 1 <= r.rating <= 5]
        if not valid_reviews:
            raise RatingValidationError("No valid ratings provided")

        return sum(r.rating for r in valid_reviews) / len(valid_reviews)

    @staticmethod
    def calculate_weighted(reviews: list[Review], weights: dict) -> float:
        """Вычисляет взвешенный рейтинг (учитывает возраст отзыва и др. факторы)"""
        # Логика расчета с учетом весов
        pass
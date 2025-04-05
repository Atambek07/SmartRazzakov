from ..domain.entities import Review
from ..domain.services import RatingCalculator
from .dto.review_dto import SubmitReviewDTO


class SubmitReviewUseCase:
    def __init__(self, review_repository, rating_calculator: RatingCalculator):
        self.repo = review_repository
        self.calculator = rating_calculator

    def execute(self, dto: SubmitReviewDTO) -> dict:
        """Обрабатывает отправку нового отзыва"""
        review = Review(
            id=None,
            author_id=dto.author_id,
            target_id=dto.target_id,
            feedback_type=dto.feedback_type,
            text=dto.text,
            rating=dto.rating,
            status="pending",
            created_at=datetime.now(),
            photos=dto.photos
        )

        saved_review = self.repo.save(review)

        # Пересчет рейтинга для target_id
        reviews = self.repo.get_for_target(dto.target_id)
        new_rating = self.calculator.calculate_average(reviews)

        return {
            "review_id": saved_review.id,
            "new_average_rating": new_rating
        }
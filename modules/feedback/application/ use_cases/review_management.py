# modules/feedback/application/use_cases/review_management.py
from typing import Optional
from abc import ABC, abstractmethod
from ...domain.entities import ReviewEntity
from ...application.dto import ReviewCreateDTO, ReviewUpdateDTO, ReviewResponseDTO
from core.utils import BaseUseCase
from core.exceptions import NotFoundException, PermissionDenied

class ReviewRepository(ABC):
    @abstractmethod
    def get_by_id(self, review_id: int) -> ReviewEntity:
        pass
    
    @abstractmethod
    def create(self, dto: ReviewCreateDTO) -> ReviewEntity:
        pass
    
    @abstractmethod
    def update(self, review_id: int, dto: ReviewUpdateDTO) -> ReviewEntity:
        pass

class CreateReviewUseCase(BaseUseCase):
    def __init__(self, repo: ReviewRepository, rating_calculator):
        self.repo = repo
        self.rating_calculator = rating_calculator

    def execute(self, dto: ReviewCreateDTO) -> ReviewResponseDTO:
        # Проверка дубликатов
        if self.repo.check_existing_review(dto.author_id, dto.object_id):
            raise ValueError("Вы уже оставляли отзыв для этого объекта")
        
        review = self.repo.create(dto)
        
        # Обновление рейтингов в связанном модуле
        self.rating_calculator.update_content_rating(
            content_type=dto.content_type,
            object_id=dto.object_id,
            module=dto.source_module
        )
        
        return ReviewResponseDTO.from_entity(review)

class UpdateReviewUseCase(BaseUseCase):
    def __init__(self, repo: ReviewRepository, rating_calculator):
        self.repo = repo
        self.rating_calculator = rating_calculator

    def execute(self, review_id: int, dto: ReviewUpdateDTO, user_id: int) -> ReviewResponseDTO:
        review = self.repo.get_by_id(review_id)
        
        if review.author_id != user_id:
            raise PermissionDenied("Только автор может редактировать отзыв")
        
        updated = self.repo.update(review_id, dto)
        
        # Обновляем рейтинги если изменилась оценка
        if dto.rating != review.rating:
            self.rating_calculator.update_content_rating(
                content_type=review.content_type,
                object_id=review.object_id,
                module=review.source_module
            )
        
        return ReviewResponseDTO.from_entity(updated)

class GetReviewUseCase(BaseUseCase):
    def __init__(self, repo: ReviewRepository):
        self.repo = repo

    def execute(self, review_id: int) -> ReviewResponseDTO:
        review = self.repo.get_by_id(review_id)
        if not review:
            raise NotFoundException("Отзыв не найден")
        return ReviewResponseDTO.from_entity(review)
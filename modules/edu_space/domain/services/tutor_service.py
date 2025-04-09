from abc import ABC, abstractmethod
from uuid import UUID
from typing import List
from ..entities import UserProfile

class TutorService(ABC):
    @abstractmethod
    def search_tutors(self, filters: dict) -> List[UserProfile]:
        """Ищет репетиторов по заданным критериям"""
        pass

    @abstractmethod
    def calculate_tutor_rating(self, tutor_id: UUID) -> float:
        """Рассчитывает рейтинг репетитора на основе отзывов"""
        pass

class BaseTutorService(TutorService):
    def __init__(self, tutor_repository, rating_calculator):
        self.tutor_repo = tutor_repository
        self.rating_calc = rating_calculator

    def calculate_tutor_rating(self, tutor_id: UUID) -> float:
        tutor = self.tutor_repo.get_by_id(tutor_id)
        return self.rating_calc.calculate(tutor.reviews)
# modules/edu_space/application/use_cases/tutor_matching.py
from uuid import UUID
from typing import List
from ...domain.repositories import TutorRepository
from ..dto.classroom_dto import CourseLevel

class TutorMatcher:
    def __init__(self, tutor_repo: TutorRepository):
        self.tutor_repo = tutor_repo

    def find_tutors(
        self,
        subjects: List[str],
        level: CourseLevel,
        max_price: float,
        min_rating: float = 4.0
    ) -> List[dict]:
        tutors = self.tutor_repo.search(
            subjects=subjects,
            min_rating=min_rating,
            max_price=max_price
        )
        
        return [{
            "id": tutor.id,
            "name": tutor.full_name,
            "rating": tutor.rating,
            "experience": tutor.years_experience,
            "price": tutor.hourly_rate,
            "subjects": tutor.subjects,
            "availability": tutor.availability
        } for tutor in tutors if self._matches_level(tutor, level)]

    def _matches_level(self, tutor, level: CourseLevel) -> bool:
        level_map = {
            'beginner': 1,
            'intermediate': 2,
            'advanced': 3
        }
        return tutor.skill_level >= level_map.get(level, 1)
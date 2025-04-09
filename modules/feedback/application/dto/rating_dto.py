# modules/feedback/application/dto/rating_dto.py
from pydantic import BaseModel, Field
from typing import Dict

class RatingCreateDTO(BaseModel):
    content_type: str = Field(
        ..., 
        example="business",
        description="Тип оцениваемого объекта"
    )
    object_id: int = Field(
        ..., 
        example=123,
        description="ID объекта в исходной системе"
    )
    average_rating: float = Field(
        ..., 
        ge=0, 
        le=5,
        example=4.5,
        description="Средний рейтинг объекта"
    )

class RatingSummaryDTO(BaseModel):
    total_reviews: int
    average_rating: float
    rating_distribution: Dict[int, int] = Field(
        ..., 
        example={1: 5, 2: 3, 3: 10, 4: 15, 5: 67},
        description="Распределение оценок по значениям"
    )
    compared_to_similar: Optional[float]

class ContentRefDTO(BaseModel):
    content_type: str
    object_id: int
    module: str

    class Config:
        schema_extra = {
            "example": {
                "content_type": "tutor",
                "object_id": 42,
                "module": "edu_space"
            }
        }
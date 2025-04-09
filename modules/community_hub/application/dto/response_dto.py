# modules/community_hub/application/dto/response_dto.py
from . import BaseCommunityDTO
from typing import Generic, TypeVar

T = TypeVar('T')

class SuccessResponse(BaseCommunityDTO, Generic[T]):
    success: bool = True
    data: T
    meta: Optional[dict] = None

class ErrorResponse(BaseCommunityDTO):
    success: bool = False
    error: str
    error_code: str
    details: Optional[dict] = None

class PaginatedResponse(SuccessResponse[T]):
    pagination: dict = {
        'total': int,
        'page': int,
        'per_page': int,
        'total_pages': int
    }
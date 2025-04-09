# modules/gov_connect/presentation/views/public_dashboard.py
from fastapi import APIRouter, Depends
from fastapi_cache.decorator import cache
from ...application.use_cases import VotingResultsUseCase
from ...infrastructure.repositories import DjangoComplaintRepository
from .schemas import PublicStatsResponse
from core.utils.responses import ErrorResponse

router = APIRouter(tags=["Public Dashboard"])

@router.get(
    "/stats",
    response_model=PublicStatsResponse,
    responses={500: {"model": ErrorResponse}}
)
@cache(expire=300)
async def get_public_stats(
    repo: DjangoComplaintRepository = Depends()
):
    """Получение публичной статистики"""
    try:
        stats = repo.get_public_stats()
        return PublicStatsResponse(**stats)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.get("/active-votings")
@cache(expire=60)
async def get_active_votings(
    use_case: VotingResultsUseCase = Depends()
):
    """Список активных голосований"""
    return use_case.get_active_votings()
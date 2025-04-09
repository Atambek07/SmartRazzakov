# modules/gov_connect/presentation/views/citizen_views.py
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from ...application.use_cases import (
    ComplaintProcessingUseCase,
    VotingCreationUseCase,
    VoteProcessingUseCase
)
from ...infrastructure.repositories import DjangoComplaintRepository
from core.authentication.permissions import IsAuthenticated, IsCitizen
from .schemas import (
    ComplaintCreateRequest,
    ComplaintStatusResponse,
    VoteRequest
)
from core.utils.responses import ErrorResponse
import logging

router = APIRouter(tags=["Citizen API"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

@router.post(
    "/complaints",
    response_model=ComplaintStatusResponse,
    responses={
        400: {"model": ErrorResponse},
        429: {"model": ErrorResponse}
    }
)
async def create_complaint(
    request: ComplaintCreateRequest,
    token: str = Depends(oauth2_scheme),
    use_case: ComplaintProcessingUseCase = Depends(),
    user: dict = Depends(IsCitizen())
):
    """Создание новой жалобы"""
    try:
        result = use_case.create_complaint(
            user_id=user['sub'],
            title=request.title,
            description=request.description,
            location=request.location.dict(),
            category=request.category,
            photos=request.photos,
            anonymous=request.anonymous
        )
        return ComplaintStatusResponse(**result)
    except Exception as e:
        logging.error(f"Complaint creation error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.post(
    "/votes",
    response_model=dict,
    dependencies=[Depends(IsAuthenticated())]
)
async def cast_vote(
    request: VoteRequest,
    use_case: VoteProcessingUseCase = Depends(),
    user: dict = Depends(IsCitizen())
):
    """Участие в голосовании"""
    try:
        return use_case.cast_vote(
            voting_id=request.voting_id,
            user_id=user['sub'],
            option=request.option
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e)
        )
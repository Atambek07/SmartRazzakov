# modules/gov_connect/presentation/views/municipal_views.py
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from ...application.use_cases import (
    ComplaintStatusUpdateUseCase,
    ComplaintModerationUseCase,
    DocumentService
)
from core.authentication.permissions import IsMunicipalWorker
from .schemas import StatusUpdateRequest, ModerationResult
from core.utils.responses import ErrorResponse
import logging

router = APIRouter(tags=["Municipal API"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

@router.patch(
    "/complaints/{complaint_id}/status",
    response_model=ModerationResult,
    responses={403: {"model": ErrorResponse}}
)
async def update_complaint_status(
    complaint_id: str,
    request: StatusUpdateRequest,
    use_case: ComplaintStatusUpdateUseCase = Depends(),
    user: dict = Depends(IsMunicipalWorker())
):
    """Обновление статуса жалобы (только для сотрудников)"""
    try:
        result = use_case.update_status(
            complaint_id=complaint_id,
            new_status=request.status,
            comment=request.comment
        )
        return ModerationResult(**result)
    except Exception as e:
        logging.error(f"Status update error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.get(
    "/reports/complaints",
    dependencies=[Depends(IsMunicipalWorker())]
)
async def generate_complaint_report(
    service: DocumentService = Depends(),
    format: str = "pdf"
):
    """Генерация отчетов по жалобам"""
    try:
        report = service.generate_complaint_report(format)
        return {"report_url": report.url}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
# modules/gov_connect/presentation/views/emergency_views.py
from fastapi import APIRouter, Depends, HTTPException
from ...application.use_cases import EmergencyBroadcastUseCase
from ...domain.entities import EmergencyAlert
from core.authentication.permissions import IsMunicipalWorker

router = APIRouter(tags=["Emergency Alerts"])

@router.post("/alerts", response_model=dict)
async def create_emergency_alert(
    alert: EmergencyAlert,
    use_case: EmergencyBroadcastUseCase = Depends(),
    _: dict = Depends(IsMunicipalWorker())
):
    try:
        result = use_case.execute(alert.dict())
        return {"status": "success", "details": result}
    except Exception as e:
        raise HTTPException(500, detail=str(e))
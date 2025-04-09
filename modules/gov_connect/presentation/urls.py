# modules/gov_connect/presentation/urls.py
from fastapi import APIRouter

from .views import emergency_views
from .views import (
    citizen_router,
    municipal_router,
    public_router
)

router = APIRouter(
    prefix="/gov-connect",
    tags=["GovConnect"],
    responses={404: {"description": "Not found"}}
)

# Подключение дочерних роутеров
router.include_router(
    citizen_router,
    prefix="/citizen",
    tags=["Citizen API"]
)

router.include_router(
    municipal_router,
    prefix="/municipal",
    tags=["Municipal API"],
    dependencies=[Depends(IsMunicipalWorker())]
)

router.include_router(
    public_router,
    prefix="/public",
    tags=["Public Dashboard"]
)

# Глобальные обработчики ошибок
@router.get("/health")
async def health_check():
    return {"status": "OK"}

router = APIRouter()
router.include_router(
    emergency_views.router,
    prefix="/emergency",
    dependencies=[Depends(IsMunicipalWorker())]
)

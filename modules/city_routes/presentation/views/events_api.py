from fastapi import APIRouter, HTTPException
from datetime import datetime
from typing import List
from domain.entities import CityEvent
from application.dto.events_dto import EventResponseDTO
from infrastructure.integrations.event_providers import CultureMapAdapter

router = APIRouter(prefix="/events", tags=["Events API"])

@router.get("/near-route/{route_id}", response_model=List[EventResponseDTO])
async def get_events_near_route(
    route_id: str,
    radius_km: int = 2,
    start_date: datetime = None,
    end_date: datetime = None
):
    """
    Получение событий в радиусе от маршрута
    Параметры:
    - radius_km: радиус поиска (по умолчанию 2 км)
    - date_range: период для фильтрации событий
    """
    try:
        adapter = CultureMapAdapter()
        return await adapter.get_events_near_route(
            route_id,
            radius_km=radius_km,
            start_date=start_date,
            end_date=end_date
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/near-point/")
async def get_events_near_point(
    lat: float,
    lon: float,
    radius_km: int = 1
):
    """Получение событий рядом с точкой"""
    try:
        adapter = CultureMapAdapter()
        return await adapter.get_events_near_location(
            lat=lat,
            lon=lon,
            radius_km=radius_km
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
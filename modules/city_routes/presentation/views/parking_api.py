from fastapi import APIRouter, HTTPException, Query
from typing import List
from domain.entities import ParkingSpot
from application.dto.parking_dto import ParkingResponseDTO
from infrastructure.integrations.parking_providers import CityParkingAdapter

router = APIRouter(prefix="/parking", tags=["Parking API"])

@router.get("/near-route/{route_id}", response_model=List[ParkingResponseDTO])
async def get_parking_near_route(
    route_id: str,
    max_distance: int = Query(500, description="Макс. расстояние в метрах"),
    vehicle_type: str = Query("car", enum=["car", "bike", "truck"])
):
    """
    Поиск парковок вдоль маршрута
    Пример ответа:
    [
        {
            "id": "park_123",
            "location": [43.256, 76.901],
            "type": "free",
            "capacity": 15,
            "distance_to_route": 250
        }
    ]
    """
    try:
        adapter = CityParkingAdapter()
        return await adapter.get_parking_along_route(
            route_id,
            max_distance_meters=max_distance,
            vehicle_type=vehicle_type
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/near-point/")
async def get_parking_near_point(
    lat: float,
    lon: float,
    radius: int = 500
):
    """Поиск парковок в радиусе от точки"""
    try:
        adapter = CityParkingAdapter()
        return await adapter.get_parking_near_location(
            lat=lat,
            lon=lon,
            radius_meters=radius
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
from fastapi import APIRouter, Depends, HTTPException
from typing import List
from domain.entities import Route, TrafficAlert
from application.dto.route_dto import RouteResponseDTO
from infrastructure.repositories import DjangoRouteRepository
from domain.services import RoutePlanner
from datetime import datetime
import uuid

router = APIRouter(prefix="/api/v1", tags=["Public API"])

# Dependency Injection
async def get_route_repo():
    return DjangoRouteRepository()

@router.post("/routes", response_model=RouteResponseDTO)
async def create_route(
    start_lat: float,
    start_lon: float,
    end_lat: float,
    end_lon: float,
    transport_type: str,
    repo: DjangoRouteRepository = Depends(get_route_repo),
    planner: RoutePlanner = Depends()
):
    """Создание нового маршрута"""
    try:
        route = await planner.calculate_route(
            start=(start_lat, start_lon),
            end=(end_lat, end_lon),
            transport_type=transport_type
        )
        saved_route = await repo.save(route)
        return saved_route
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/routes/nearby", response_model=List[RouteResponseDTO])
async def get_nearby_routes(
    lat: float,
    lon: float,
    radius_km: float = 5.0,
    repo: DjangoRouteRepository = Depends(get_route_repo)
):
    """Получение маршрутов в радиусе"""
    return await repo.find_nearby(
        location=(lat, lon),
        radius_km=radius_km
    )

@router.get("/routes/{route_id}", response_model=RouteResponseDTO)
async def get_route_details(
    route_id: uuid.UUID,
    repo: DjangoRouteRepository = Depends(get_route_repo)
):
    """Получение деталей маршрута"""
    try:
        return await repo.get_by_id(route_id)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
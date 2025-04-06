from fastapi import APIRouter, HTTPException, Depends
from typing import List
from domain.entities import WeatherPoint
from application.dto.weather_dto import WeatherResponseDTO
from domain.services.weather_service import WeatherService
from infrastructure.integrations.weather_providers import OpenWeatherMapAdapter

router = APIRouter(prefix="/weather", tags=["Weather API"])

async def get_weather_service():
    return WeatherService(OpenWeatherMapAdapter(api_key="your_api_key"))

@router.get("/route/{route_id}", response_model=List[WeatherResponseDTO])
async def get_route_weather(
    route_id: str,
    weather_service: WeatherService = Depends(get_weather_service)
):
    """
    Получение погоды вдоль маршрута с шагом 5 км
    Пример ответа:
    [
        {
            "point": [43.256, 76.901],
            "temperature": 25.3,
            "conditions": "clear",
            "precipitation_prob": 0
        }
    ]
    """
    try:
        return await weather_service.get_route_weather(route_id, step_km=5)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/point/")
async def get_point_weather(
    lat: float = Query(..., ge=-90, le=90),
    lon: float = Query(..., ge=-180, le=180),
    weather_service: WeatherService = Depends(get_weather_service)
):
    """Получение погоды в конкретной точке"""
    try:
        return await weather_service.get_point_weather(lat, lon)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
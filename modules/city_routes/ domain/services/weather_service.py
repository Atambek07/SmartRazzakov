# domain/services/weather_service.py
from abc import ABC, abstractmethod

class WeatherService(ABC):
    @abstractmethod
    async def get_route_weather(self, route_id: str, step_km: int):
        pass
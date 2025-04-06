# application/dto/weather_dto.py
from pydantic import BaseModel

class WeatherResponseDTO(BaseModel):
    point: list[float]
    temperature: float
    conditions: str
    precipitation_prob: float
    wind_speed: float
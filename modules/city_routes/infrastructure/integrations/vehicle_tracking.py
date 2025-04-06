import asyncio
from typing import Dict, List, Optional
from dataclasses import dataclass
from domain.entities import TransportVehicle

@dataclass
class VehiclePosition:
    vehicle_id: str
    lat: float
    lon: float
    speed: float
    timestamp: int

class YandexTrackerAdapter:
    def __init__(self, oauth_token: str, counter_id: str):
        self.base_url = "https://api.tracker.yandex.net"
        self.headers = {
            "Authorization": f"OAuth {oauth_token}",
            "X-Org-ID": counter_id
        }

    async def get_vehicles_positions(self) -> Dict[str, VehiclePosition]:
        """Получение данных с трекеров Яндекс.Трекер"""
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/v2/vehicles",
                headers=self.headers
            )
            data = response.json()
            return {
                item['vehicle_id']: VehiclePosition(
                    vehicle_id=item['vehicle_id'],
                    lat=item['position']['lat'],
                    lon=item['position']['lon'],
                    speed=item['position']['speed'],
                    timestamp=item['position']['timestamp']
                )
                for item in data['vehicles']
            }

class GPSGateTracker:
    """Интеграция с системой GPSGate"""
    def __init__(self, api_key: str):
        self.api_key = api_key

    async def get_available_vehicles(
        self,
        location: tuple[float, float],
        radius_km: float = 5.0
    ) -> List[TransportVehicle]:
        """Получение доступного транспорта в радиусе"""
        pass
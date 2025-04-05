import requests
from django.conf import settings
from typing import List, Tuple


class OSMService:
    def __init__(self):
        self.base_url = "https://router.project-osrm.org/route/v1/driving/"

    def get_route_coordinates(self, start: Tuple[float, float], end: Tuple[float, float]) -> List[Tuple[float, float]]:
        """Получает точки маршрута от OSM"""
        url = f"{self.base_url}{start[1]},{start[0]};{end[1]},{end[0]}?overview=full"

        try:
            response = requests.get(url, timeout=10)
            data = response.json()
            return self._decode_polyline(data['routes'][0]['geometry'])
        except Exception as e:
            raise ConnectionError(f"OSM API error: {str(e)}")

    def _decode_polyline(self, polyline_str: str) -> List[Tuple[float, float]]:
        """Декодирует полилинию OSM в координаты"""
        # ... (реализация декодирования)
        return decoded_coords
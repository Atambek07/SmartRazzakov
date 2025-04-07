import requests
from typing import Tuple, Optional
import logging
from django.conf import settings

logger = logging.getLogger(__name__)


class ElevationService:
    """
    Сервис работы с высотой над уровнем моря
    Использует Google Maps Elevation API
    """

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or getattr(settings, 'GOOGLE_MAPS_API_KEY', '')
        self.base_url = "https://maps.googleapis.com/maps/api/elevation/json"

    def get_elevation(self, point: Tuple[float, float]) -> Optional[float]:
        """
        Получение высоты для координаты (широта, долгота)
        :return: Высота в метрах или None при ошибке
        """
        try:
            params = {
                'locations': f"{point[0]},{point[1]}",
                'key': self.api_key
            }
            response = requests.get(self.base_url, params=params)
            data = response.json()

            if data.get('status') == 'OK':
                return data['results'][0]['elevation']
            return None

        except Exception as e:
            logger.error(f"Elevation request failed: {str(e)}")
            return None

    def get_elevation_profile(
            self,
            path: List[Tuple[float, float]],
            samples: int = 100
    ) -> List[dict]:
        """
        Получение профиля высот для маршрута
        :return: [{'lat': float, 'lng': float, 'elevation': float}]
        """
        try:
            locations = "|".join(f"{p[0]},{p[1]}" for p in path)
            params = {
                'path': locations,
                'samples': samples,
                'key': self.api_key
            }
            response = requests.get(self.base_url, params=params)
            return response.json().get('results', [])

        except Exception as e:
            logger.error(f"Elevation profile failed: {str(e)}")
            return []
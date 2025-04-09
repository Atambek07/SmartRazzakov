# modules/gov_connect/infrastructure/integrations/gis_integration.py
import requests
from abc import ABC, abstractmethod
from typing import Tuple, Optional
import logging
from cachetools import cached, TTLCache

logger = logging.getLogger(__name__)

class GISAdapter(ABC):
    @abstractmethod
    def validate_coordinates(self, lat: float, lng: float) -> bool:
        pass
    
    @abstractmethod
    def reverse_geocode(self, lat: float, lng: float) -> Optional[str]:
        pass

class GoogleMapsGIS(GISAdapter):
    BASE_URL = "https://maps.googleapis.com/maps/api"
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.cache = TTLCache(maxsize=1000, ttl=3600)

    @cached(cache=TTLCache(maxsize=1000, ttl=3600))
    def validate_coordinates(self, lat: float, lng: float) -> bool:
        try:
            response = requests.get(
                f"{self.BASE_URL}/geocode/json",
                params={
                    "latlng": f"{lat},{lng}",
                    "key": self.api_key
                },
                timeout=5
            )
            return response.json().get('status') == 'OK'
        except Exception as e:
            logger.error(f"GIS validation error: {str(e)}")
            return False

    def reverse_geocode(self, lat: float, lng: float) -> Optional[str]:
        try:
            response = requests.get(
                f"{self.BASE_URL}/geocode/json",
                params={
                    "latlng": f"{lat},{lng}",
                    "key": self.api_key,
                    "language": "ru"
                },
                timeout=5
            )
            results = response.json().get('results')
            return results[0]['formatted_address'] if results else None
        except Exception as e:
            logger.error(f"Reverse geocoding error: {str(e)}")
            return None

class OpenStreetMapGIS(GISAdapter):
    BASE_URL = "https://nominatim.openstreetmap.org"
    
    def validate_coordinates(self, lat: float, lng: float) -> bool:
        return -90 <= lat <= 90 and -180 <= lng <= 180

    def reverse_geocode(self, lat: float, lng: float) -> Optional[str]:
        try:
            response = requests.get(
                f"{self.BASE_URL}/reverse",
                params={
                    "lat": lat,
                    "lon": lng,
                    "format": "json",
                    "accept-language": "ru"
                },
                headers={'User-Agent': 'GovConnect/1.0'},
                timeout=5
            )
            data = response.json()
            return data.get('display_name')
        except Exception as e:
            logger.error(f"OSM geocoding error: {str(e)}")
            return None
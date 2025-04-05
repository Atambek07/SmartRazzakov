from django.core.cache import caches
from ..domain.entities import TransportRoute
from .models import TransportRoute as RouteModel


class DjangoRouteRepository:
    def __init__(self):
        self.cache = caches['routes']

    def get_available_routes(self, start: str, end: str) -> List[TransportRoute]:
        cache_key = f"routes_{start}_{end}"
        routes = self.cache.get(cache_key)

        if not routes:
            routes = self._fetch_from_db(start, end)
            self.cache.set(cache_key, routes, timeout=300)

        return routes

    def _fetch_from_db(self, start: str, end: str) -> List[TransportRoute]:
        """Преобразует Django ORM модели в доменные entities"""
        db_routes = RouteModel.objects.filter(
            stops__dwithin=(start_point, 0.1)  # Пример пространственного запроса
        ).select_related('vehicles')

        return [
            TransportRoute(
                id=str(route.id),
                transport_type=route.vehicle_type,
                number=route.number,
                stops=self._parse_stops(route.stops),
                schedule=route.schedule,
                current_location=self._get_latest_location(route.vehicles.all())
            ) for route in db_routes
        ]
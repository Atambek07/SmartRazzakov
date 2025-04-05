from django.contrib.gis.geos import Point
from ..models.route_model import TransportRoute
from domain.entities import TransportRoute as DomainRoute


class DjangoRouteRepository:
    def get_available_routes(self, start: tuple, end: tuple) -> list[DomainRoute]:
        """Получает маршруты между точками с преобразованием в доменные объекты"""
        start_point = Point(start[1], start[0])  # (longitude, latitude)
        end_point = Point(end[1], end[0])

        routes = TransportRoute.objects.filter(
            stops__contains=start_point
        )

        return [
            DomainRoute(
                id=str(route.id),
                number=route.number,
                transport_type=route.transport_type,
                stops=self._parse_stops(route.stops),
                schedule=route.schedule,
                price=float(route.price),
                estimated_time=route.estimated_time
            ) for route in routes
        ]

    def _parse_stops(self, line_string) -> list[str]:
        """Преобразует LineString в список ID остановок"""
        # Реальная реализация зависит от вашей структуры данных
        return [f"stop_{i}" for i in range(len(line_string))]
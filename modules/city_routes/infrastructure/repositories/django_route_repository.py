from typing import List, Optional
from uuid import UUID
from django.contrib.gis.geos import LineString, Point
from django.db import transaction
from domain.entities import Route, TransportType
from domain.exceptions import RouteNotFoundError
from ..models import RouteModel, Location, RoutePoint
from .route_repo import RouteRepository

class DjangoRouteRepository(RouteRepository):
    """Реализация репозитория маршрутов на Django ORM"""

    async def get_by_id(self, route_id: UUID) -> Route:
        try:
            route = await RouteModel.objects.aget(pk=route_id)
            return self._to_domain_entity(route)
        except RouteModel.DoesNotExist as e:
            raise RouteNotFoundError(route_id) from e

    @transaction.atomic
    async def save(self, route: Route) -> Route:
        # Создаем или обновляем точки маршрута
        start_loc = await Location.objects.acreate(
            point=Point(route.start_point[1], route.start_point[0])
        )
        end_loc = await Location.objects.acreate(
            point=Point(route.end_point[1], route.end_point[0])
        )

        # Создаем LineString из waypoints
        waypoints = [Point(lon, lat) for lat, lon in route.waypoints]
        path = LineString(waypoints, srid=4326)

        defaults = {
            'start_point': start_loc,
            'end_point': end_loc,
            'path': path,
            'distance_km': route.distance_km,
            'estimated_duration_min': route.estimated_duration_min,
            'is_active': True
        }

        route_model, created = await RouteModel.objects.aupdate_or_create(
            id=route.id,
            defaults=defaults
        )

        # Сохраняем промежуточные точки
        await self._save_route_points(route_model, route.waypoints)
        
        return self._to_domain_entity(route_model)

    async def _save_route_points(self, route_model: RouteModel, waypoints: list):
        await RoutePoint.objects.filter(route=route_model).adelete()
        for order, (lat, lon) in enumerate(waypoints[1:-1], start=1):
            loc = await Location.objects.acreate(point=Point(lon, lat))
            await RoutePoint.objects.acreate(
                route=route_model,
                location=loc,
                order=order
            )

    async def delete(self, route_id: UUID) -> None:
        deleted = await RouteModel.objects.filter(pk=route_id).adelete()
        if deleted[0] == 0:
            raise RouteNotFoundError(route_id)

    async def find_by_criteria(
        self,
        start_point: Optional[tuple[float, float]] = None,
        end_point: Optional[tuple[float, float]] = None,
        transport_type: Optional[str] = None,
        max_distance: Optional[float] = None
    ) -> List[Route]:
        from django.db.models import Q
        query = Q(is_active=True)

        if start_point:
            lat, lon = start_point
            query &= Q(start_point__point__dwithin=(Point(lon, lat), 0.01))  # ~1km

        if end_point:
            lat, lon = end_point
            query &= Q(end_point__point__dwithin=(Point(lon, lat), 0.01))

        if transport_type:
            query &= Q(transport_type=transport_type)

        if max_distance:
            query &= Q(distance_km__lte=max_distance)

        routes = []
        async for route in RouteModel.objects.filter(query).prefetch_related('points'):
            routes.append(self._to_domain_entity(route))
        return routes

    def _to_domain_entity(self, route_model: RouteModel) -> Route:
        waypoints = [
            (route_model.start_point.point.y, route_model.start_point.point.x)
        ]
        
        # Добавляем промежуточные точки в правильном порядке
        for point in sorted(route_model.points.all(), key=lambda p: p.order):
            waypoints.append((point.location.point.y, point.location.point.x))
        
        waypoints.append((route_model.end_point.point.y, route_model.end_point.point.x))

        return Route(
            id=route_model.id,
            start_point=(route_model.start_point.point.y, route_model.start_point.point.x),
            end_point=(route_model.end_point.point.y, route_model.end_point.point.x),
            waypoints=waypoints,
            distance_km=route_model.distance_km,
            estimated_duration_min=route_model.estimated_duration_min,
            transport_type=TransportType(route_model.transport_type),
            created_at=route_model.created_at
        )
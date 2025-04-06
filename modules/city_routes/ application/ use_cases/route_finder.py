from typing import Optional
from city_routes.domain.entities import Route
from city_routes.domain.exceptions import RouteNotFound
from city_routes.domain.services.route_planner import RoutePlanner
from city_routes.application.dto.route_dto import RouteRequestDTO, RouteResponseDTO


class RouteFinderUseCase:
    def __init__(self, route_planner: RoutePlanner, repository):
        self.route_planner = route_planner
        self.repository = repository

    async def find_route(self, request: RouteRequestDTO) -> RouteResponseDTO:
        try:
            route = await self.route_planner.calculate_route(
                start=(request.start_lat, request.start_lon),
                end=(request.end_lat, request.end_lon),
                transport_type=request.transport,
                options={
                    'avoid_tolls': request.avoid_tolls,
                    'wheelchair_accessible': request.wheelchair_accessible
                }
            )

            saved_route = await self.repository.save(route)

            return RouteResponseDTO(
                route_id=str(saved_route.id),
                distance_km=saved_route.distance_km,
                duration_min=saved_route.estimated_duration_min,
                polyline=saved_route.waypoints,
                transport_type=request.transport,
                created_at=saved_route.created_at,
                eco_score=self._calculate_eco_score(saved_route),
                accessibility_features=self._get_accessibility_features(saved_route)
            )
        except Exception as e:
            raise RouteNotFound(f"Route calculation failed: {str(e)}") from e

    def _calculate_eco_score(self, route: Route) -> float:
        # Логика расчета экологичности маршрута
        base_scores = {
            'bus': 8.5,
            'metro': 9.0,
            'bike': 10.0,
            'pedestrian': 10.0,
            'taxi': 4.0
        }
        return base_scores.get(route.transport_type, 5.0)

    def _get_accessibility_features(self, route: Route) -> list[str]:
        # Логика определения доступности
        features = []
        if route.wheelchair_accessible:
            features.append("wheelchair")
        if route.has_elevators:
            features.append("elevator")
        return features
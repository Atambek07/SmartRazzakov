import aiohttp
from typing import List, Tuple
from domain.services.route_planner import RoutePlanner
from domain.exceptions import RouteOptimizationError

class OSMAdapter(RoutePlanner):
    OSM_ROUTING_URL = "https://router.project-osrm.org/route/v1"

    async def calculate_route(
        self,
        start: Tuple[float, float],
        end: Tuple[float, float],
        transport_type: TransportType,
        options: Optional[dict] = None
    ) -> Route:
        profile = self._get_osm_profile(transport_type)
        url = f"{self.OSM_ROUTING_URL}/{profile}/{start[1]},{start[0]};{end[1]},{end[0]}"

        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url) as response:
                    data = await response.json()
                    return self._parse_osm_response(data, start, end, transport_type)
            except Exception as e:
                raise RouteOptimizationError(f"OSM routing failed: {str(e)}")

    def _get_osm_profile(self, transport_type: TransportType) -> str:
        profiles = {
            TransportType.PEDESTRIAN: "foot",
            TransportType.BIKE: "bike",
            TransportType.BUS: "car",
            TransportType.TAXI: "car"
        }
        return profiles.get(transport_type, "car")

    def _parse_osm_response(self, data: dict, start: Tuple[float, float], end: Tuple[float, float], 
                          transport_type: TransportType) -> Route:
        if data.get('code') != 'Ok':
            raise RouteOptimizationError(data.get('message', 'Unknown OSM error'))

        return Route(
            start_point=start,
            end_point=end,
            waypoints=[(point[1], point[0]) for point in data['waypoints']],
            distance_km=data['routes'][0]['distance'] / 1000,
            estimated_duration_min=data['routes'][0]['duration'] / 60,
            transport_type=transport_type
        )
import httpx
from typing import Optional, Dict
from domain.entities import Route, TransportType
from domain.services.route_planner import RoutePlanner
from domain.exceptions import RouteOptimizationError

class MapboxProvider(RoutePlanner):
    def __init__(self, api_key: str):
        self.base_url = "https://api.mapbox.com/directions/v5"
        self.api_key = api_key
        self.client = httpx.AsyncClient(timeout=30.0)

    async def calculate_route(
        self,
        start: tuple[float, float],
        end: tuple[float, float],
        transport_type: TransportType,
        options: Optional[dict] = None
    ) -> Route:
        profile = {
            TransportType.PEDESTRIAN: "walking",
            TransportType.BIKE: "cycling",
            TransportType.BUS: "driving-traffic",
            TransportType.TAXI: "driving"
        }.get(transport_type, "driving")

        params = {
            "access_token": self.api_key,
            "geometries": "geojson",
            "steps": "true",
            "overview": "full"
        }

        if options:
            if options.get("wheelchair_accessible"):
                params["annotations"] = "wheelchair"
            if options.get("avoid_tolls"):
                params["avoid"] = "tolls"

        try:
            response = await self.client.get(
                f"{self.base_url}/mapbox/{profile}/{start[1]},{start[0]};{end[1]},{end[0]}",
                params=params
            )
            data = response.json()
            
            return Route(
                start_point=start,
                end_point=end,
                waypoints=[(coord[1], coord[0]) for coord in data['routes'][0]['geometry']['coordinates']],
                distance_km=data['routes'][0]['distance'] / 1000,
                estimated_duration_min=data['routes'][0]['duration'] / 60,
                transport_type=transport_type,
                wheelchair_accessible=options.get("wheelchair_accessible", False)
            )
        except Exception as e:
            raise RouteOptimizationError(f"Mapbox routing failed: {str(e)}")

    async def close(self):
        await self.client.aclose()
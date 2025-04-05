from ..entities import TransportRoute, RouteOptimization


class RoutePlanner:
    def __init__(self, map_provider):
        self.map_provider = map_provider

    def plan_route(self, start: str, end: str, optimization: RouteOptimization) -> TransportRoute:
        """Планирует маршрут с учетом выбранной оптимизации"""
        routes = self.map_provider.get_available_routes(start, end)

        if optimization == RouteOptimization.FASTEST:
            return min(routes, key=lambda r: r.estimated_time)
        elif optimization == RouteOptimization.CHEAPEST:
            return min(routes, key=lambda r: r.price)
        else:  # ECO
            return min(routes, key=lambda r: r.carbon_footprint)
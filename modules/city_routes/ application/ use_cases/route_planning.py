from ..domain.entities import RouteOptimization


class GetRouteUseCase:
    def __init__(self, repository):
        self.repo = repository

    def execute(self, start: str, end: str, optimization: str) -> 'TransportRoute':
        """Возвращает оптимальный маршрут"""
        routes = self.repo.get_available_routes(start, end)

        if not routes:
            raise ValueError("Нет доступных маршрутов")

        optimization = RouteOptimization(optimization.lower())

        if optimization == RouteOptimization.FASTEST:
            return min(routes, key=lambda r: r.estimated_time)
        elif optimization == RouteOptimization.CHEAPEST:
            return min(routes, key=lambda r: r.price)
        else:  # ECO
            return min(routes, key=lambda r: r.eco_score)
from ..domain.entities import RouteOptimization
from ..domain.services import RouteCalculator


class RouteFinderUseCase:
    def __init__(self, route_calculator: RouteCalculator):
        self.calculator = route_calculator

    def find_optimal_route(self, start: Tuple[float, float],
                           end: Tuple[float, float],
                           optimization: RouteOptimization) -> dict:
        routes = self.calculator.get_available_routes(start, end)

        if optimization == RouteOptimization.FASTEST:
            best_route = min(routes, key=lambda x: x.estimated_time)
        elif optimization == RouteOptimization.CHEAPEST:
            best_route = min(routes, key=lambda x: x.price)
        else:  # ECO
            best_route = min(routes, key=lambda x: x.eco_score)

        return {
            'route_number': best_route.number,
            'stops': best_route.stops,
            'estimated_time': best_route.estimated_time,
            'price': best_route.price
        }
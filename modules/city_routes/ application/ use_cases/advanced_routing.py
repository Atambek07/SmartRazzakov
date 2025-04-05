from ..domain.entities import RouteOptimization
from ..domain.services import RouteCalculator
from typing import List, Dict


class OptimizedRouteFinder:
    def __init__(self, route_calculator: RouteCalculator):
        self.calculator = route_calculator

    def execute(self, points: List[Dict], optimization: RouteOptimization) -> Dict:
        """
        points: [{'coords': (lat, lng), 'type': 'start|end|via'}]
        optimization: FASTEST|CHEAPEST|ECO
        """
        routes = []

        # Генерация всех возможных комбинаций маршрутов
        for i in range(len(points) - 1):
            start = points[i]['coords']
            end = points[i + 1]['coords']
            segment_routes = self.calculator.get_routes_between(start, end)
            routes.append(segment_routes)

        # Применение алгоритма оптимизации
        if optimization == RouteOptimization.FASTEST:
            return self._find_fastest_combination(routes)
        elif optimization == RouteOptimization.CHEAPEST:
            return self._find_cheapest_combination(routes)
        else:
            return self._find_eco_friendly_combination(routes)

    def _find_fastest_combination(self, route_options: List[List]) -> Dict:
        """Использует алгоритм Дейкстры для поиска самого быстрого маршрута"""
        # ... реализация алгоритма
        return best_route
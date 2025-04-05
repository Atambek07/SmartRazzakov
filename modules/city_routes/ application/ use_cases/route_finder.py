from typing import Literal
from domain.entities import TransportRoute


class RouteFinderUseCase:
    def execute(self,
                start: tuple[float, float],
                end: tuple[float, float],
                optimization: Literal['fastest', 'cheapest', 'eco']) -> TransportRoute:
        """Основной сценарий поиска маршрута"""
        routes = self.repository.get_available_routes(start, end)

        if not routes:
            raise ValueError("Нет доступных маршрутов")

        if optimization == 'fastest':
            return min(routes, key=lambda r: r.estimated_time)
        elif optimization == 'cheapest':
            return min(routes, key=lambda r: r.price)
        else:  # eco
            return self._find_most_eco_route(routes)

    def _find_most_eco_route(self, routes: list[TransportRoute]) -> TransportRoute:
        """Находит самый экологичный маршрут (примерная реализация)"""
        return sorted(
            routes,
            key=lambda r: {'bus': 3, 'tram': 1, 'trolley': 2, 'minibus': 4}[r.transport_type]
        )[0]
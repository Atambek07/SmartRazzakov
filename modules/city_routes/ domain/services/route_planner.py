from abc import ABC, abstractmethod
from ..entities import Route
from ..exceptions import InvalidCoordinatesError


class RoutePlanner(ABC):
    """Абстрактный сервис для построения маршрутов."""

    @abstractmethod
    def find_optimal_route(self, start: str, end: str, mode: str = "driving") -> Route:
        """
        Находит оптимальный маршрут между точками.

        :param start: Координаты начальной точки (формат: "lat,lng").
        :param end: Координаты конечной точки.
        :param mode: Тип маршрута ("driving", "walking", "public").
        :return: Объект Route.
        :raises InvalidCoordinatesError: Если координаты некорректны.
        """
        pass

    @abstractmethod
    def calculate_distance(self, point1: str, point2: str) -> float:
        """Вычисляет расстояние между двумя точками в км."""
        pass
from abc import ABC, abstractmethod
from typing import List, Tuple
from ..entities import Route, TransportType
from ..exceptions import RouteOptimizationError

class RouteOptimizer(ABC):
    """Абстрактный сервис оптимизации маршрутов"""
    
    @abstractmethod
    async def optimize_route(
        self,
        route: Route,
        constraints: Optional[Dict] = None
    ) -> Route:
        """
        Оптимизирует существующий маршрут с учетом ограничений
        Args:
            route: исходный маршрут
            constraints: словарь ограничений (avoid_areas, max_distance и т.д.)
        Returns:
            Оптимизированный маршрут
        """
        pass

    @abstractmethod
    async def find_alternatives(
        self,
        route: Route,
        max_alternatives: int = 3
    ) -> List[Route]:
        """
        Находит альтернативные маршруты
        Args:
            route: исходный маршрут
            max_alternatives: максимальное количество альтернатив
        Returns:
            Список альтернативных маршрутов
        """
        pass

    @abstractmethod
    async def multi_route_plan(
        self,
        points: List[Tuple[float, float]],
        transport: TransportType
    ) -> List[Route]:
        """
        Строит маршрут через несколько точек
        Args:
            points: список точек, которые нужно посетить
            transport: тип транспорта
        Returns:
            Оптимальный порядок посещения точек
        """
        pass
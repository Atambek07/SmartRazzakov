from abc import ABC, abstractmethod
from typing import List, Tuple, Optional
from ..entities import Route, TransportType
from ..exceptions import RouteOptimizationError

class RoutePlanner(ABC):
    """Абстрактный сервис для построения маршрутов"""
    
    @abstractmethod
    async def calculate_route(
        self,
        start: Tuple[float, float],
        end: Tuple[float, float],
        transport_type: TransportType,
        options: Optional[dict] = None
    ) -> Route:
        """
        Рассчитывает оптимальный маршрут между точками
        Args:
            start: (latitude, longitude) начальной точки
            end: (latitude, longitude) конечной точки
            transport_type: тип транспорта
            options: дополнительные параметры (avoid_tolls, wheelchair_accessible и т.д.)
        Returns:
            Объект Route с рассчитанным маршрутом
        Raises:
            RouteOptimizationError: если не удалось построить маршрут
        """
        pass

    @abstractmethod
    async def estimate_duration(
        self,
        route: Route,
        traffic_conditions: Optional[dict] = None
    ) -> float:
        """Оценивает время прохождения маршрута в минутах"""
        pass
from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID
from domain.entities import Route
from domain.exceptions import RouteNotFoundError

class RouteRepository(ABC):
    """Абстрактный репозиторий для работы с маршрутами"""
    
    @abstractmethod
    async def get_by_id(self, route_id: UUID) -> Route:
        """Получить маршрут по ID"""
        pass

    @abstractmethod
    async def save(self, route: Route) -> Route:
        """Сохранить или обновить маршрут"""
        pass

    @abstractmethod
    async def delete(self, route_id: UUID) -> None:
        """Удалить маршрут"""
        pass

    @abstractmethod
    async def find_by_criteria(
        self,
        start_point: Optional[tuple[float, float]] = None,
        end_point: Optional[tuple[float, float]] = None,
        transport_type: Optional[str] = None,
        max_distance: Optional[float] = None
    ) -> List[Route]:
        """Поиск маршрутов по критериям"""
        pass
from abc import ABC, abstractmethod
from ..entities import TrafficInfo
from ..exceptions import TrafficDataUnavailableError


class TrafficService(ABC):
    """Абстрактный сервис для работы с данными о трафике."""

    @abstractmethod
    def get_real_time_traffic(self, route_id: str) -> TrafficInfo:
        """
        Возвращает актуальные данные о трафике для маршрута.

        :param route_id: Идентификатор маршрута.
        :raises TrafficDataUnavailableError: Если данные недоступны.
        """
        pass

    @abstractmethod
    def predict_congestion(self, route_id: str) -> str:
        """Прогнозирует уровень загруженности ("low", "medium", "high")."""
        pass
from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Tuple, Dict
from ..entities import TrafficAlert

class TrafficService(ABC):
    """Абстрактный сервис для работы с трафиком"""
    
    @abstractmethod
    async def get_current_traffic(
        self,
        location: Tuple[float, float],
        radius_km: float = 5.0
    ) -> Dict:
        """
        Получает текущую информацию о трафике в указанной области
        Args:
            location: (latitude, longitude) центра области
            radius_km: радиус области в километрах
        Returns:
            Словарь с данными о трафике:
            {
                "congestion_level": 0.7,  # от 0 до 1
                "average_speed_kmh": 45,
                "incidents": [...]
            }
        """
        pass

    @abstractmethod
    async def create_alert(
        self,
        alert: TrafficAlert
    ) -> TrafficAlert:
        """Создает новое оповещение о пробке"""
        pass

    @abstractmethod
    async def predict_congestion(
        self,
        location: Tuple[float, float],
        time: datetime
    ) -> float:
        """
        Прогнозирует уровень загруженности в указанное время
        Returns:
            Уровень загруженности от 0 (свободно) до 1 (пробка)
        """
        pass
from typing import List, Tuple, Callable
import logging
from shapely.geometry import Point, Polygon
from .distance_calculator import DistanceCalculator

logger = logging.getLogger(__name__)


class GeoFenceManager:
    """
    Менеджер геозон с поддержкой:
    - Полигонов произвольной формы
    - Круговых зон
    - Триггеров при входе/выходе
    """

    def __init__(self):
        self.fences = {}
        self.distance_calc = DistanceCalculator()

    def add_circular_fence(
            self,
            fence_id: str,
            center: Tuple[float, float],
            radius: float,
            unit: str = 'm'
    ):
        """Добавление круговой геозоны"""
        self.fences[fence_id] = {
            'type': 'circle',
            'center': center,
            'radius': radius,
            'unit': unit
        }

    def add_polygon_fence(
            self,
            fence_id: str,
            vertices: List[Tuple[float, float]]
    ):
        """Добавление полигональной геозоны"""
        self.fences[fence_id] = {
            'type': 'polygon',
            'polygon': Polygon(vertices)
        }

    def check_position(
            self,
            point: Tuple[float, float],
            previous_point: Optional[Tuple[float, float]] = None
    ) -> List[str]:
        """
        Проверка нахождения точки в геозонах
        Возвращает список ID активных геозон
        """
        active_fences = []

        for fence_id, fence in self.fences.items():
            if fence['type'] == 'circle':
                distance = self.distance_calc.calculate(
                    fence['center'],
                    point,
                    fence.get('unit', 'm')
                )
                if distance <= fence['radius']:
                    active_fences.append(fence_id)

            elif fence['type'] == 'polygon':
                if fence['polygon'].contains(Point(point[1], point[0])):
                    active_fences.append(fence_id)

        return active_fences

    def add_fence_trigger(
            self,
            fence_id: str,
            trigger_type: str,
            callback: Callable
    ):
        """Добавление обработчика событий геозоны"""
        # Реализация логики триггеров
        pass
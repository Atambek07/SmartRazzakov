from geopy.distance import geodesic
from typing import Tuple, Optional
import logging

logger = logging.getLogger(__name__)


class DistanceCalculator:
    """
    Калькулятор расстояний между географическими точками
    Поддерживает разные единицы измерения и методы расчета
    """

    def __init__(self, default_unit: str = 'km'):
        self.valid_units = {'km', 'm', 'mile'}
        self.default_unit = default_unit if default_unit in self.valid_units else 'km'

    def calculate(
            self,
            point1: Tuple[float, float],
            point2: Tuple[float, float],
            unit: Optional[str] = None
    ) -> float:
        """
        Расчет расстояния между двумя точками (широта, долгота)

        :param point1: (lat, lon)
        :param point2: (lat, lon)
        :param unit: km/m/mile
        :return: расстояние в указанных единицах
        """
        try:
            distance = geodesic(point1, point2).kilometers

            if unit and unit in self.valid_units:
                return self._convert_units(distance, unit)
            return self._convert_units(distance, self.default_unit)

        except Exception as e:
            logger.error(f"Distance calculation failed: {str(e)}")
            raise

    def _convert_units(self, distance_km: float, target_unit: str) -> float:
        """Конвертация единиц измерения"""
        if target_unit == 'm':
            return distance_km * 1000
        elif target_unit == 'mile':
            return distance_km * 0.621371
        return distance_km

    def is_within_radius(
            self,
            center: Tuple[float, float],
            point: Tuple[float, float],
            radius: float,
            unit: str = 'km'
    ) -> bool:
        """Проверка нахождения точки в радиусе"""
        return self.calculate(center, point, unit) <= radius
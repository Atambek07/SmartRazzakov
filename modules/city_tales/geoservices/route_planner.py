import osmnx as ox
from typing import List, Tuple, Optional
import logging
from .distance_calculator import DistanceCalculator

logger = logging.getLogger(__name__)


class RoutePlanner:
    """
    Планировщик маршрутов с использованием OpenStreetMap данных
    Поддерживает пешеходные, вело- и авто-маршруты
    """

    def __init__(self, city_name: str = "Москва"):
        try:
            self.graph = ox.graph_from_place(
                city_name,
                network_type='walk',
                simplify=True
            )
            self.distance_calculator = DistanceCalculator()
        except Exception as e:
            logger.error(f"Failed to initialize route planner: {str(e)}")
            raise

    def get_route(
            self,
            start: Tuple[float, float],
            end: Tuple[float, float],
            route_type: str = 'walk'
    ) -> dict:
        """
        Построение маршрута между точками

        :param start: (lat, lon)
        :param end: (lat, lon)
        :param route_type: walk/bike/drive
        :return: {
            'path': List[coordinates],
            'distance': float (km),
            'duration': float (minutes)
        }
        """
        try:
            # Получение ближайших узлов графа
            start_node = ox.nearest_nodes(self.graph, start[1], start[0])
            end_node = ox.nearest_nodes(self.graph, end[1], end[0])

            # Расчет маршрута
            route = ox.shortest_path(
                self.graph,
                start_node,
                end_node,
                weight='length'
            )

            # Извлечение координат
            path = [
                (self.graph.nodes[node]['y'], self.graph.nodes[node]['x'])
                for node in route
            ]

            # Расчет расстояния и времени
            distance = sum(
                ox.utils_graph.get_route_edge_attributes(
                    self.graph,
                    route,
                    'length'
                )
            ) / 1000  # в км

            duration = distance / self._get_speed(route_type) * 60  # в минутах

            return {
                'path': path,
                'distance': round(distance, 2),
                'duration': round(duration, 1)
            }

        except Exception as e:
            logger.error(f"Route planning failed: {str(e)}")
            raise

    def _get_speed(self, route_type: str) -> float:
        """Скорость передвижения (км/ч)"""
        speeds = {
            'walk': 5,
            'bike': 15,
            'drive': 40
        }
        return speeds.get(route_type, 5)
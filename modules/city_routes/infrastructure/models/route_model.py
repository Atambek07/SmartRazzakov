from django.contrib.gis.db import models
from core.models.base import BaseModel

class RouteModel(BaseModel):
    """Модель маршрута с геоданными (LineString)."""
    name = models.CharField(max_length=255)
    start_point = models.PointField()  # Точка старта (latitude, longitude)
    end_point = models.PointField()    # Точка финиша
    path = models.LineStringField()    # Геометрия маршрута
    distance_km = models.FloatField()  # Дистанция в км
    duration_min = models.IntegerField()  # Время в минутах

    class Meta:
        db_table = 'routes'
        verbose_name = 'Маршрут'
        verbose_name_plural = 'Маршруты'

    def __init__(self):
        self.id = None

    def __str__(self):
        return f"Маршрут #{self.id}: {self.name}"
from django.contrib.gis.db import models
from core.models.base import BaseModel

class TrafficModel(BaseModel):
    """Модель данных о трафике для участка маршрута."""
    CONGESTION_LEVELS = [
        ('low', 'Низкая'),
        ('medium', 'Средняя'),
        ('high', 'Высокая'),
    ]

    route = models.ForeignKey(
        'RouteModel',
        on_delete=models.CASCADE,
        related_name='traffic_data'
    )
    segment = models.LineStringField()  # Геометрия проблемного участка
    congestion_level = models.CharField(
        max_length=10,
        choices=CONGESTION_LEVELS
    )
    average_speed_kmh = models.FloatField()  # Средняя скорость

    class Meta:
        db_table = 'traffic'
        verbose_name = 'Данные о трафике'
        verbose_name_plural = 'Данные о трафике'

    def __str__(self):
        return f"Трафик на маршруте #{self.route_id}: {self.get_congestion_level_display()}"
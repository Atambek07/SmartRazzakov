from django.contrib.gis.db import models
from django.db import transaction
from django.core.validators import MinValueValidator
from .gis import Location

class RouteModel(models.Model):
    """
    Модель маршрута с геоданными для хранения в PostgreSQL/PostGIS
    """
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name="ID маршрута"
    )
    start_point = models.ForeignKey(
        Location,
        on_delete=models.PROTECT,
        related_name='start_routes',
        verbose_name="Точка старта"
    )
    end_point = models.ForeignKey(
        Location,
        on_delete=models.PROTECT,
        related_name='end_routes',
        verbose_name="Точка финиша"
    )
    path = models.LineStringField(
        srid=4326,
        verbose_name="Геометрия маршрута"
    )
    distance_km = models.FloatField(
        validators=[MinValueValidator(0)],
        verbose_name="Расстояние (км)"
    )
    estimated_duration_min = models.FloatField(
        validators=[MinValueValidator(0)],
        verbose_name="Расчетное время (минуты)"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Дата обновления"
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Активный маршрут"
    )

    class Meta:
        verbose_name = "Маршрут"
        verbose_name_plural = "Маршруты"
        indexes = [
            models.Index(fields=['start_point', 'end_point']),
            models.Index(fields=['created_at']),
        ]
        ordering = ['-created_at']

    def __str__(self):
        return f"Маршрут {self.id} ({self.distance_km} км)"

    @transaction.atomic
    def save(self, *args, **kwargs):
        # Автоматический расчет длины при сохранении
        if self.path and not self.distance_km:
            self.distance_km = self.path.length * 100  # Примерный коэффициент
        super().save(*args, **kwargs)

class RoutePoint(models.Model):
    """
    Промежуточные точки маршрута
    """
    route = models.ForeignKey(
        RouteModel,
        on_delete=models.CASCADE,
        related_name='points',
        verbose_name="Маршрут"
    )
    location = models.ForeignKey(
        Location,
        on_delete=models.PROTECT,
        verbose_name="Точка маршрута"
    )
    order = models.PositiveIntegerField(
        verbose_name="Порядковый номер"
    )
    stop_duration_min = models.FloatField(
        default=0,
        validators=[MinValueValidator(0)],
        verbose_name="Время остановки (минуты)"
    )

    class Meta:
        verbose_name = "Точка маршрута"
        verbose_name_plural = "Точки маршрута"
        ordering = ['route', 'order']
        unique_together = ['route', 'order']

    def __str__(self):
        return f"Точка {self.order} маршрута {self.route_id}"
from django.contrib.gis.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class TransportTypeModel(models.Model):
    """
    Тип транспортного средства
    """
    name = models.CharField(
        max_length=50,
        unique=True,
        verbose_name="Название типа"
    )
    code = models.CharField(
        max_length=20,
        unique=True,
        verbose_name="Кодовое обозначение"
    )
    speed_kmh = models.FloatField(
        validators=[MinValueValidator(0)],
        verbose_name="Средняя скорость (км/ч)"
    )
    eco_class = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(5)],
        verbose_name="Экологический класс"
    )
    icon = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Иконка"
    )

    class Meta:
        verbose_name = "Тип транспорта"
        verbose_name_plural = "Типы транспорта"

    def __str__(self):
        return self.name

class TransportVehicleModel(models.Model):
    """
    Модель транспортного средства с геолокацией
    """
    id = models.CharField(
        primary_key=True,
        max_length=50,
        verbose_name="Идентификатор"
    )
    type = models.ForeignKey(
        TransportTypeModel,
        on_delete=models.PROTECT,
        verbose_name="Тип транспорта"
    )
    current_location = models.PointField(
        srid=4326,
        verbose_name="Текущее местоположение"
    )
    last_update = models.DateTimeField(
        auto_now=True,
        verbose_name="Последнее обновление"
    )
    capacity = models.PositiveIntegerField(
        default=1,
        verbose_name="Вместимость"
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Активен"
    )
    license_plate = models.CharField(
        max_length=20,
        blank=True,
        verbose_name="Гос. номер"
    )
    properties = models.JSONField(
        default=dict,
        blank=True,
        verbose_name="Дополнительные свойства"
    )

    class Meta:
        verbose_name = "Транспортное средство"
        verbose_name_plural = "Транспортные средства"
        indexes = [
            models.Index(fields=['type']),
            models.Index(fields=['is_active']),
            models.Index(fields=['current_location']),
        ]

    def __str__(self):
        return f"{self.type} {self.license_plate or self.id}"
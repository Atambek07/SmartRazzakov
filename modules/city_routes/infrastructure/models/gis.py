from django.contrib.gis.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Location(models.Model):
    """
    Модель географического местоположения с поддержкой PostGIS
    """
    point = models.PointField(
        srid=4326,  # WGS84
        verbose_name="Координаты (широта, долгота)"
    )
    address = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Адрес"
    )
    city = models.CharField(
        max_length=100,
        default="Раззаков",
        verbose_name="Город"
    )
    postal_code = models.CharField(
        max_length=20,
        blank=True,
        verbose_name="Почтовый индекс"
    )
    accuracy_m = models.FloatField(
        validators=[MinValueValidator(0)],
        null=True,
        blank=True,
        verbose_name="Точность (метры)"
    )

    class Meta:
        verbose_name = "Местоположение"
        verbose_name_plural = "Местоположения"
        indexes = [
            models.Index(fields=['point']),
            models.Index(fields=['city']),
        ]

    def __str__(self):
        return f"{self.city}, {self.address or 'точка на карте'}"
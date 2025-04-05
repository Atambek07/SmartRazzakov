from django.contrib.gis.db import models
from django.db.models import JSONField


class TransportRoute(models.Model):
    number = models.CharField(max_length=10, unique=True)
    transport_type = models.CharField(max_length=10)
    stops = models.LineStringField()
    schedule = JSONField(default=dict)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    estimated_time = models.PositiveIntegerField()  # minutes

    class Meta:
        indexes = [
            models.Index(fields=['number']),
            models.Index(fields=['transport_type']),
        ]

    def __str__(self):
        return f"Маршрут {self.number} ({self.transport_type})"
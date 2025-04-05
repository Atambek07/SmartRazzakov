from django.db import models
from django.contrib.gis.db import models as gis_models


class TransportVehicle(models.Model):
    VEHICLE_TYPES = [
        ('bus', 'Автобус'),
        ('tram', 'Трамвай'),
        ('trolley', 'Троллейбус'),
        ('minibus', 'Маршрутка')
    ]

    number = models.CharField(max_length=10)
    vehicle_type = models.CharField(max_length=10, choices=VEHICLE_TYPES)
    current_location = gis_models.PointField()
    last_update = models.DateTimeField(auto_now=True)
    route = models.ForeignKey('TransportRoute', on_delete=models.CASCADE)

    class Meta:
        indexes = [
            models.Index(fields=['vehicle_type']),
            models.Index(fields=['number']),
        ]


class TransportRoute(models.Model):
    number = models.CharField(max_length=10, unique=True)
    stops = gis_models.LineStringField()  # Маршрут как линия на карте
    schedule = models.JSONField()  # {"weekdays": [...], "weekends": [...]}
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f"Маршрут {self.number}"
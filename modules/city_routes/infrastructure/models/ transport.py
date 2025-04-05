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
    capacity = models.IntegerField(default=30)
    route = models.ForeignKey('TransportRoute', on_delete=models.CASCADE)


class TransportRoute(models.Model):
    number = models.CharField(max_length=10)
    stops = gis_models.LineStringField()
    schedule = models.JSONField()  # {weekdays: [], weekends: []}
    price = models.DecimalField(max_digits=6, decimal_places=2)
    is_active = models.BooleanField(default=True)
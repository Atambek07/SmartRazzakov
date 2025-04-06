from django.db import models
from django.contrib.gis.db import models as gis_models


class TransportVehicle(models.Model):
    VEHICLE_TYPES = [
        ('bus', 'Автобус'),
        ('minibus', 'Маршрутка')
    ]

    vehicle_type = models.CharField(max_length=20, choices=VEHICLE_TYPES)
    current_location = models.PointField()  # Текущие координаты
    route = models.ForeignKey(
        'RouteModel',
        on_delete=models.CASCADE,
        related_name='transports'
    )
    last_update = models.DateTimeField(auto_now=True)
    speed_kmh = models.FloatField(default=0)  # Текущая скорость

    class Meta:
        db_table = 'transports'
        verbose_name = 'Транспорт'
        verbose_name_plural = 'Транспортные средства'

    def __str__(self):
        return f"{self.get_vehicle_type_display()} #{self.id}"
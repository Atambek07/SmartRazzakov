    # modules/gov_connect/infrastructure/models/emergency.py
from django.contrib.gis.db import models
from django.contrib.postgres.fields import JSONField

class EmergencyAlertModel(models.Model):
    id = models.UUIDField(primary_key=True)
    message = models.TextField()
    alert_type = models.CharField(max_length=50)
    zones = JSONField()
    channels = JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='pending')

    class Meta:
        db_table = "emergency_alerts"

class EmergencyZoneModel(models.Model):
    id = models.UUIDField(primary_key=True)
    name = models.CharField(max_length=255)
    geojson = models.GeometryField()
    population = models.IntegerField()
    priority = models.IntegerField()

    class Meta:
        db_table = "emergency_zones"
        indexes = [models.Index(fields=['priority'])]
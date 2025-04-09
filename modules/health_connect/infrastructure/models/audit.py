# modules/health_connect/models/audit.py
from django.db import models

class MedicalRecordAudit(models.Model):
    record = models.ForeignKey('MedicalRecord', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    action = models.CharField(max_length=50)
    changes = models.JSONField()
    timestamp = models.DateTimeField(auto_now_add=True)

# Сигналы для отслеживания изменений
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=MedicalRecord)
def log_medical_record_change(sender, instance, created, **kwargs):
    action = 'CREATE' if created else 'UPDATE'
    MedicalRecordAudit.objects.create(
        record=instance,
        user=instance.last_modified_by,
        action=action,
        changes=instance.get_changes()
    )
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class PatientProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    blood_type = models.CharField(max_length=3)
    allergies = models.JSONField(default=list)
    chronic_diseases = models.JSONField(default=list)


class MedicalRecord(models.Model):
    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='records')
    diagnosis = models.CharField(max_length=200)
    treatment = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    doctor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='authored_records')
    is_emergency = models.BooleanField(default=False)
    attachments = models.JSONField(default=list)


class Appointment(models.Model):
    STATUS_CHOICES = [
        ('scheduled', 'Запланирован'),
        ('completed', 'Завершен'),
        ('cancelled', 'Отменен')
    ]

    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='patient_appointments')
    doctor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='doctor_appointments')
    datetime = models.DateTimeField()
    duration = models.PositiveIntegerField()  # минуты
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='scheduled')
    video_link = models.URLField(null=True, blank=True)
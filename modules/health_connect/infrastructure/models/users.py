# modules/health_connect/infrastructure/models/users.py
from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinLengthValidator
from core.models import BaseModel
import uuid

class PatientProfile(BaseModel):
    user = models.OneToOneField(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='patient_profile'
    )
    national_id = models.CharField(
        max_length=20,
        unique=True,
        validators=[MinLengthValidator(10)]
    )
    blood_type = models.CharField(
        max_length=3,
        choices=[
            ('A+', 'A+'), ('A-', 'A-'),
            ('B+', 'B+'), ('B-', 'B-'),
            ('AB+', 'AB+'), ('AB-', 'AB-'),
            ('O+', 'O+'), ('O-', 'O-')
        ],
        null=True
    )
    height = models.PositiveSmallIntegerField(null=True, help_text="In centimeters")
    weight = models.FloatField(null=True, help_text="In kilograms")
    emergency_contact = models.JSONField(default=dict)
    insurance_info = models.JSONField(default=dict)
    is_verified = models.BooleanField(default=False)

    class Meta:
        indexes = [
            models.Index(fields=['national_id']),
            models.Index(fields=['blood_type']),
        ]

class HealthcareProviderProfile(BaseModel):
    user = models.OneToOneField(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='provider_profile'
    )
    license_number = models.CharField(
        max_length=20,
        unique=True,
        validators=[MinLengthValidator(8)]
    )
    specializations = models.JSONField(default=list)
    facilities = models.ManyToManyField(
        'health_connect.MedicalFacility',
        related_name='providers'
    )
    available_hours = models.JSONField(default=dict)
    languages = models.JSONField(default=list)
    is_verified = models.BooleanField(default=False)
    consultation_fee = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True
    )

    class Meta:
        indexes = [
            models.Index(fields=['license_number']),
        ]
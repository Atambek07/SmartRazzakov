# modules/health_connect/infrastructure/models/medical.py
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from core.models import BaseModel
import uuid

class MedicalRecord(BaseModel):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    patient = models.ForeignKey(
        'PatientProfile',
        on_delete=models.CASCADE,
        related_name='medical_records'
    )
    record_type = models.CharField(
        max_length=20,
        choices=[
            ('allergy', 'Allergy'),
            ('diagnosis', 'Diagnosis'),
            ('prescription', 'Prescription'),
            ('vaccination', 'Vaccination'),
            ('procedure', 'Procedure'),
            ('lab_result', 'Lab Result'),
            ('imaging', 'Imaging'),
            ('clinical_note', 'Clinical Note')
        ]
    )
    title = models.CharField(max_length=200)
    content = models.JSONField()
    provider = models.ForeignKey(
        'HealthcareProviderProfile',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    is_confidential = models.BooleanField(default=False)
    related_appointment = models.ForeignKey(
        'Appointment',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    class Meta:
        indexes = [
            models.Index(fields=['record_type']),
            models.Index(fields=['is_confidential']),
        ]
        ordering = ['-created_at']

class Appointment(BaseModel):
    STATUS_CHOICES = [
        ('requested', 'Requested'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('rescheduled', 'Rescheduled')
    ]

    patient = models.ForeignKey(
        'PatientProfile',
        on_delete=models.CASCADE,
        related_name='appointments'
    )
    provider = models.ForeignKey(
        'HealthcareProviderProfile',
        on_delete=models.CASCADE,
        related_name='appointments'
    )
    scheduled_time = models.DateTimeField()
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='requested'
    )
    duration = models.PositiveSmallIntegerField(
        default=30,
        validators=[
            MinValueValidator(15),
            MaxValueValidator(120)
        ]
    )
    reason = models.TextField(null=True, blank=True)
    video_link = models.URLField(null=True, blank=True)
    meeting_id = models.CharField(max_length=100, null=True, blank=True)
    cancellation_reason = models.TextField(null=True, blank=True)

    class Meta:
        indexes = [
            models.Index(fields=['scheduled_time']),
            models.Index(fields=['status']),
        ]
        ordering = ['scheduled_time']

class MedicalFacility(BaseModel):
    name = models.CharField(max_length=200)
    address = models.JSONField()
    contact_info = models.JSONField()
    facility_type = models.CharField(
        max_length=50,
        choices=[
            ('hospital', 'Hospital'),
            ('clinic', 'Clinic'),
            ('pharmacy', 'Pharmacy'),
            ('lab', 'Diagnostic Lab')
        ]
    )
    services = models.JSONField(default=list)
    operating_hours = models.JSONField(default=dict)
    is_approved = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Medical Facilities"
        indexes = [
            models.Index(fields=['facility_type']),
        ]
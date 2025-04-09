# modules/health_connect/admin.py
from django.contrib import admin
from .models import (
    PatientProfile,
    HealthcareProviderProfile,
    MedicalRecord,
    Appointment,
    MedicalFacility
)

class MedicalRecordInline(admin.StackedInline):
    model = MedicalRecord
    extra = 0
    fields = ('record_type', 'title', 'created_at')
    readonly_fields = ('created_at',)

@admin.register(PatientProfile)
class PatientProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'national_id', 'blood_type', 'is_verified')
    search_fields = ('user__username', 'national_id')
    list_filter = ('blood_type', 'is_verified')
    inlines = [MedicalRecordInline]
    fieldsets = (
        (None, {'fields': ('user', 'national_id')}),
        ('Медицинская информация', {'fields': (
            'blood_type', 
            'height', 
            'weight'
        )}),
        ('Контакты', {'fields': ('emergency_contact',)}),
        ('Статус', {'fields': ('is_verified',)})
    )

@admin.register(HealthcareProviderProfile)
class HealthcareProviderAdmin(admin.ModelAdmin):
    list_display = ('user', 'license_number', 'consultation_fee', 'is_verified')
    search_fields = ('user__username', 'license_number')
    list_filter = ('specializations', 'is_verified')
    filter_horizontal = ('facilities',)
    fieldsets = (
        (None, {'fields': ('user', 'license_number')}),
        ('Профессиональная информация', {'fields': (
            'specializations',
            'facilities',
            'available_hours'
        )}),
        ('Финансы', {'fields': ('consultation_fee',)}),
        ('Статус', {'fields': ('is_verified',)})
    )

@admin.register(MedicalRecord)
class MedicalRecordAdmin(admin.ModelAdmin):
    list_display = ('patient', 'record_type', 'created_at', 'is_confidential')
    list_filter = ('record_type', 'is_confidential')
    search_fields = ('title', 'content')
    date_hierarchy = 'created_at'
    readonly_fields = ('created_at', 'modified_at')

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('patient', 'provider', 'scheduled_time', 'status')
    list_filter = ('status', 'scheduled_time')
    search_fields = ('patient__user__username', 'provider__user__username')
    date_hierarchy = 'scheduled_time'

@admin.register(MedicalFacility)
class MedicalFacilityAdmin(admin.ModelAdmin):
    list_display = ('name', 'facility_type', 'is_approved')
    list_filter = ('facility_type', 'is_approved')
    search_fields = ('name', 'address')
    filter_horizontal = ('services',)
# modules/health_connect/presentation/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    MedicalRecordViewSet,
    PatientAppointmentViewSet,
    DoctorScheduleAPIView,
    ConfirmAppointmentAPIView,
    EmergencyRequestAPIView,
    EmergencyProvidersAPIView
)

# Инициализация роутера для ViewSets
router = DefaultRouter()
router.register(
    r'medical-records', 
    MedicalRecordViewSet, 
    basename='medical-records'
)
router.register(
    r'appointments', 
    PatientAppointmentViewSet, 
    basename='patient-appointments'
)

urlpatterns = [
    # Пациентские эндпоинты
    path('patient/', include([
        path('', include(router.urls)),
        path(
            'appointments/<uuid:pk>/cancel/', 
            PatientAppointmentViewSet.as_view({'post': 'cancel'}), 
            name='cancel-appointment'
        )
    ])),
    
    # Врачебные эндпоинты
    path('doctor/', include([
        path(
            'schedule/', 
            DoctorScheduleAPIView.as_view(), 
            name='doctor-schedule'
        ),
        path(
            'appointments/<uuid:appointment_id>/confirm/', 
            ConfirmAppointmentAPIView.as_view(), 
            name='confirm-appointment'
        )
    ])),
    
    # Экстренные эндпоинты
    path('emergency/', include([
        path(
            'request/', 
            EmergencyRequestAPIView.as_view(), 
            name='emergency-request'
        ),
        path(
            'providers/', 
            EmergencyProvidersAPIView.as_view(), 
            name='emergency-providers'
        )
    ])),
    
    # Документация OpenAPI
    path(
        'swagger/', 
        get_swagger_view(title='HealthConnect API'), 
        name='swagger-docs'
    )
]

# Добавление namespace для модуля
app_name = 'healthconnect-api'
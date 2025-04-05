from django.urls import path
from .presentation.views import (
    PublicTransportAPI,
    VehicleLocationAPI,
    SMSRouteInfoAPI
)

urlpatterns = [
    path('plan-route/', PublicTransportAPI.as_view(), name='plan-route'),
    path('vehicle/<int:vehicle_id>/', VehicleLocationAPI.as_view(), name='vehicle-location'),
    path('sms/route-info/', SMSRouteInfoAPI.as_view(), name='sms-route-info'),
]
from django.urls import path
from .views import RouteAPIView, VehicleLocationAPIView

urlpatterns = [
    path('routes/', RouteAPIView.as_view(), name='route-finder'),
    path('vehicles/<int:vehicle_id>/',
         VehicleLocationAPIView.as_view(),
         name='vehicle-location'),
]
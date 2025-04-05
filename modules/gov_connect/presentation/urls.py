from django.urls import path
from .presentation.views import (
    CitizenComplaintAPI,
    ComplaintStatusAPI,
    MunicipalServicesAPI
)

urlpatterns = [
    path('complaints/', CitizenComplaintAPI.as_view(), name='submit-complaint'),
    path('complaints/<int:pk>/status/', ComplaintStatusAPI.as_view(), name='update-status'),
    path('services/', MunicipalServicesAPI.as_view(), name='municipal-services'),
]
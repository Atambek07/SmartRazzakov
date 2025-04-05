from rest_framework_simplejwt.tokens import AccessToken
from django.utils import timezone
from datetime import timedelta

class SmartCityAccessToken(AccessToken):
    @property
    def lifetime(self):
        if self.payload.get('is_service_account'):
            return timedelta(days=30)  # Longer expiry for service accounts
        return timedelta(minutes=15)   # Standard expiry
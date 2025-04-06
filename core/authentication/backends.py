from rest_framework_simplejwt.authentication import JWTAuthentication
from oauth2_provider.contrib.rest_framework import OAuth2Authentication
from rest_framework.exceptions import AuthenticationFailed
from django.conf import settings

from datetime import timedelta
from oauth2_provider.models import Application

def get_jwt_tokens(user):
    app = Application.objects.get(name="SmartCityApp")
    return {
        "token_type": "Bearer",
        "expires_in": 3600,
        "access_token": generate_access_token(user, app),
        "refresh_token": generate_refresh_token(user, app),
    }

class HybridAuthBackend(JWTAuthentication, OAuth2Authentication):
    """
    Hybrid authentication backend supporting both JWT and OAuth2
    """
    def authenticate(self, request):
        # Try JWT first
        try:
            return JWTAuthentication.authenticate(self, request)
        except Exception:
            pass

        # Fallback to OAuth2
        try:
            return OAuth2Authentication.authenticate(self, request)
        except Exception:
            return None

    def get_user(self, validated_token):
        if isinstance(validated_token, dict):  # JWT case
            return super(JWTAuthentication, self).get_user(validated_token)
        return validated_token.user  # OAuth case
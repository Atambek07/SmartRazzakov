import json
import logging
from django.http import JsonResponse
from rest_framework import status

logger = logging.getLogger(__name__)


class APIErrorHandler:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_exception(self, request, exception):
        logger.error(f"API Error: {str(exception)}", exc_info=True)

        error_data = {
            'status': 'error',
            'code': status.HTTP_500_INTERNAL_SERVER_ERROR,
            'message': 'Internal server error',
            'details': str(exception)
        }

        return JsonResponse(error_data, status=500)
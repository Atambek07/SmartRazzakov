# core/middleware/analytics.py
import time
import logging

logger = logging.getLogger(__name__)

class UserActivityMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start_time = time.time()
        response = self.get_response(request)
        duration = time.time() - start_time

        user_data = {
            'user_id': request.user.id if request.user.is_authenticated else None,
            'path': request.path,
            'method': request.method,
            'status_code': response.status_code,
            'duration': duration,
            'timestamp': time.time(),
        }

        logger.info("User activity", extra=user_data)
        return response
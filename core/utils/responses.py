from rest_framework.response import Response


class APIResponse(Response):
    """
    Standardized API response format
    """

    def __init__(self, data=None, status=None,
                 template_name=None, headers=None,
                 exception=False, content_type=None,
                 **kwargs):
        response_data = {
            'status': 'success' if status < 400 else 'error',
            'data': data,
            **kwargs
        }

        super().__init__(
            data=response_data,
            status=status,
            template_name=template_name,
            headers=headers,
            exception=exception,
            content_type=content_type
        )
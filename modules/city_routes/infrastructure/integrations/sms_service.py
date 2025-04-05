import requests
from django.conf import settings
from typing import Literal

SMSType = Literal['route_info', 'delay_alert', 'emergency']


class SMSGateway:
    def __init__(self):
        self.provider_url = settings.SMS_PROVIDER_URL
        self.api_key = settings.SMS_API_KEY

    def send_sms(self, phone: str, message_type: SMSType, data: dict) -> bool:
        templates = {
            'route_info': (
                f"Маршрут {data['number']}: "
                f"Следующая остановка {data['next_stop']}, "
                f"Прибытие через {data['eta']} мин"
            ),
            'delay_alert': (
                f"Внимание! Маршрут {data['number']} задерживается. "
                f"Новое время прибытия: {data['new_time']}"
            )
        }

        payload = {
            "phone": phone,
            "text": templates[message_type],
            "sender": "SmartRazakov"
        }

        response = requests.post(
            self.provider_url,
            json=payload,
            headers={"Authorization": f"Bearer {self.api_key}"}
        )

        return response.status_code == 200
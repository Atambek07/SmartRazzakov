import requests
from django.conf import settings


class SMSNotifier:
    def __init__(self):
        self.api_url = settings.SMS_GATEWAY_URL
        self.api_key = settings.SMS_API_KEY

    def send_route_info(self, phone: str, route_info: dict) -> bool:
        """Отправляет информацию о маршруте через SMS"""
        text = (
            f"Маршрут {route_info['number']}:\n"
            f"Остановки: {route_info['stops']}\n"
            f"Время прибытия: {route_info['arrival_time']}"
        )

        response = requests.post(
            self.api_url,
            json={
                "phone": phone,
                "text": text,
                "sender": "SmartRazakov"
            },
            headers={"Authorization": f"Bearer {self.api_key}"}
        )

        return response.status_code == 200
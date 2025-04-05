import requests
from django.conf import settings

class LocalBankPaymentGateway:
    def __init__(self):
        self.api_url = settings.LOCAL_BANK_API_URL
        self.auth_token = settings.LOCAL_BANK_AUTH_TOKEN

    def create_payment(self, amount: float, order_id: str) -> dict:
        """Инициирует платеж через местный банк"""
        response = requests.post(
            f"{self.api_url}/payments",
            json={
                "amount": amount,
                "reference": order_id,
                "currency": "KGS"
            },
            headers={"Authorization": f"Bearer {self.auth_token}"}
        )
        return response.json()
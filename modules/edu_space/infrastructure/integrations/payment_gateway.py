from abc import ABC, abstractmethod
from typing import Optional, Dict
from django.conf import settings
import stripe
import paypalrestsdk
import httpx

class PaymentError(Exception):
    """Базовое исключение для ошибок платежей"""
    def __init__(self, message: str, code: str):
        super().__init__(message)
        self.code = code

class BasePaymentGateway(ABC):
    @abstractmethod
    async def create_payment_intent(
        self, 
        amount: float,
        currency: str = "KGZ",
        metadata: Optional[Dict] = None
    ) -> Dict:
        pass

    @abstractmethod
    async def confirm_payment(self, payment_id: str) -> Dict:
        pass

class StripeGateway(BasePaymentGateway):
    def __init__(self):
        stripe.api_key = settings.STRIPE_API_KEY
        self.client = stripe

    async def create_payment_intent(self, amount, currency="KGZ", metadata=None):
        try:
            intent = self.client.PaymentIntent.create(
                amount=int(amount * 100),
                currency=currency.lower(),
                metadata=metadata or {},
                payment_method_types=["card"],
            )
            return {
                "id": intent.id,
                "client_secret": intent.client_secret,
                "status": intent.status
            }
        except stripe.error.StripeError as e:
            raise PaymentError(str(e), code=e.code)

    async def confirm_payment(self, payment_id):
        try:
            intent = self.client.PaymentIntent.retrieve(payment_id)
            return {
                "id": intent.id,
                "status": intent.status,
                "amount": intent.amount / 100
            }
        except stripe.error.StripeError as e:
            raise PaymentError(str(e), code=e.code)

class PayPalGateway(BasePaymentGateway):
    def __init__(self):
        paypalrestsdk.configure({
            "mode": settings.PAYPAL_MODE,
            "client_id": settings.PAYPAL_CLIENT_ID,
            "client_secret": settings.PAYPAL_SECRET
        })

    async def create_payment_intent(self, amount, currency="KGZ", metadata=None):
        payment = paypalrestsdk.Payment({
            "intent": "sale",
            "payer": {"payment_method": "paypal"},
            "transactions": [{
                "amount": {
                    "total": str(amount),
                    "currency": currency
                },
                "description": metadata.get("description", "")
            }],
            "redirect_urls": {
                "return_url": settings.PAYPAL_RETURN_URL,
                "cancel_url": settings.PAYPAL_CANCEL_URL
            }
        })

        if payment.create():
            return {
                "id": payment.id,
                "approval_url": next(link.href for link in payment.links if link.method == "REDIRECT")
            }
        else:
            raise PaymentError(payment.error, code="PAYPAL_ERROR")

    async def confirm_payment(self, payment_id):
        payment = paypalrestsdk.Payment.find(payment_id)
        if payment.execute({"payer_id": payment.payer.payer_info.payer_id}):
            return {
                "id": payment.id,
                "status": payment.state,
                "amount": float(payment.transactions[0].amount.total)
            }
        raise PaymentError(payment.error, code="PAYPAL_EXECUTE_ERROR")

class PaymentGatewayFactory:
    @staticmethod
    def get_gateway(name: str = "stripe") -> BasePaymentGateway:
        gateways = {
            "stripe": StripeGateway,
            "paypal": PayPalGateway
        }
        return gateways[name.lower()]()
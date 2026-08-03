import requests
from django.conf import settings


class PaystackService:

    BASE_URL = "https://api.paystack.co"

    @staticmethod
    def initialize_payment(order):

        url = f"{PaystackService.BASE_URL}/transaction/initialize"

        headers = {
            "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}",
            "Content-Type": "application/json",
        }

        payload = {
            "email": order.email,
            "amount": int(order.total_amount * 100),  # Convert KES to cents
            "reference": order.order_number,
            "callback_url": settings.PAYSTACK_CALLBACK_URL,
        }

        response = requests.post(
            url,
            json=payload,
            headers=headers,
        )

        return response.json()

    @staticmethod
    def verify_payment(reference):

        url = f"{PaystackService.BASE_URL}/transaction/verify/{reference}"

        headers = {
            "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}",
        }

        response = requests.get(
            url,
            headers=headers,
        )

        return response.json()
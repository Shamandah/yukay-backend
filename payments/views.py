from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from orders.models import Order
from .services import PaystackService


class InitializePaymentAPIView(APIView):

    def post(self, request):

        order_id = request.data.get("order_id")

        if not order_id:
            return Response(
                {"error": "order_id is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            order = Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            return Response(
                {"error": "Order not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        paystack_response = PaystackService.initialize_payment(order)

        return Response(
            paystack_response,
            status=status.HTTP_200_OK,
        )
    
class VerifyPaymentAPIView(APIView):

    def get(self, request, reference):

        paystack_response = PaystackService.verify_payment(reference)

        if (
            paystack_response.get("status")
            and paystack_response["data"]["status"] == "success"
        ):

            order = Order.objects.get(order_number=reference)

            order.status = "PAID"
            order.save()

        return Response(
            paystack_response,
            status=status.HTTP_200_OK,
        )

# Create your views here.

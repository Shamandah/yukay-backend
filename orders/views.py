import uuid
from decimal import Decimal

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from cart.models import Cart
from .models import Order, OrderItem
from .serializers import OrderSerializer


class CheckoutAPIView(APIView):

    def post(self, request):

        session_key = request.session.session_key

        if not session_key:
            return Response(
                {"error": "Cart not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        try:
            cart = Cart.objects.get(session_key=session_key)
        except Cart.DoesNotExist:
            return Response(
                {"error": "Cart not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        if not cart.items.exists():
            return Response(
                {"error": "Your cart is empty."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        order = Order.objects.create(
            order_number=f"YUKAY-{uuid.uuid4().hex[:8].upper()}",
            customer_name=request.data["customer_name"],
            phone_number=request.data["phone_number"],
            email=request.data.get("email", ""),
            delivery_method=request.data["delivery_method"],
            delivery_address=request.data.get("delivery_address", ""),
            payment_method=request.data["payment_method"],
            special_instructions=request.data.get(
                "special_instructions",
                "",
            ),
            total_amount=Decimal("0.00"),
        )

        total = Decimal("0.00")

        for item in cart.items.all():

            subtotal = item.menu_item.price * item.quantity

            OrderItem.objects.create(
                order=order,
                menu_item=item.menu_item,
                quantity=item.quantity,
                price=item.menu_item.price,
                subtotal=subtotal,
            )

            total += subtotal

        order.total_amount = total
        order.save()

        cart.items.all().delete()

        serializer = OrderSerializer(order)

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
        )
# Create your views here.

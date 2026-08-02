from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Cart, CartItem
from menu.models import MenuItem
from .serializers import CartSerializer


class AddToCartAPIView(APIView):

    def post(self, request):

        session_key = request.session.session_key

        if not session_key:
            request.session.create()
            session_key = request.session.session_key

        cart, created = Cart.objects.get_or_create(
            session_key=session_key
        )

        menu_item = get_object_or_404(
            MenuItem,
            id=request.data.get("menu_item"),
        )

        quantity = int(request.data.get("quantity", 1))

        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            menu_item=menu_item,
            defaults={"quantity": quantity},
        )

        if not created:
            cart_item.quantity += quantity
            cart_item.save()

        serializer = CartSerializer(cart)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )
class CartAPIView(APIView):

    def get(self, request):

        session_key = request.session.session_key

        if not session_key:
            return Response(
                {"message": "Cart is empty"},
                status=status.HTTP_200_OK,
            )

        try:
            cart = Cart.objects.get(session_key=session_key)
        except Cart.DoesNotExist:
            return Response(
                {"message": "Cart is empty"},
                status=status.HTTP_200_OK,
            )

        serializer = CartSerializer(cart)

        return Response(serializer.data)
class UpdateCartItemAPIView(APIView):

    def patch(self, request, item_id):

        cart_item = get_object_or_404(
            CartItem,
            id=item_id,
        )

        quantity = int(request.data.get("quantity", 1))

        if quantity <= 0:
            return Response(
                {"error": "Quantity must be greater than zero."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        cart_item.quantity = quantity
        cart_item.save()

        serializer = CartSerializer(cart_item.cart)

        return Response(serializer.data)
class RemoveCartItemAPIView(APIView):

    def delete(self, request, item_id):

        cart_item = get_object_or_404(
            CartItem,
            id=item_id,
        )

        cart_item.delete()

        return Response(
            {"message": "Item removed successfully."},
            status=status.HTTP_200_OK,
        )
class ClearCartAPIView(APIView):

    def delete(self, request):

        session_key = request.session.session_key

        if not session_key:
            return Response(
                {"message": "Cart already empty."},
                status=status.HTTP_200_OK,
            )

        try:
            cart = Cart.objects.get(session_key=session_key)
        except Cart.DoesNotExist:
            return Response(
                {"message": "Cart already empty."},
                status=status.HTTP_200_OK,
            )

        cart.items.all().delete()

        return Response(
            {"message": "Cart cleared successfully."},
            status=status.HTTP_200_OK,
        )
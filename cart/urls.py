from django.urls import path
from .views import AddToCartAPIView, CartAPIView, UpdateCartItemAPIView, RemoveCartItemAPIView, ClearCartAPIView

urlpatterns = [
    path("add/", AddToCartAPIView.as_view(), name="add-to-cart"),
    path("", CartAPIView.as_view(), name="cart"),
    path("item/<int:item_id>/", UpdateCartItemAPIView.as_view(), name="update-cart-item"),
    path(
    "item/<int:item_id>/delete/",
    RemoveCartItemAPIView.as_view(),
    name="remove-cart-item",
),
path(
    "clear/",
    ClearCartAPIView.as_view(),
    name="clear-cart",
),
]
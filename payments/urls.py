from django.urls import path
from .views import InitializePaymentAPIView

urlpatterns = [
    path(
        "initialize/",
        InitializePaymentAPIView.as_view(),
        name="initialize-payment",
    ),
    path(
        "verify/<str:reference>/",
        InitializePaymentAPIView.as_view(),
        name="verify-payment",
    ),

]
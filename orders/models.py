from django.db import models


class Order(models.Model):

    STATUS_CHOICES = [
        ("PENDING", "Pending"),
        ("PAID", "Paid"),
        ("PREPARING", "Preparing"),
        ("READY", "Ready for Pickup"),
        ("OUT_FOR_DELIVERY", "Out for Delivery"),
        ("DELIVERED", "Delivered"),
        ("CANCELLED", "Cancelled"),
    ]

    PAYMENT_CHOICES = [
        ("MPESA", "M-Pesa"),
        ("PAYSTACK", "Paystack"),
        ("PAY_ON_PICKUP", "Pay on Pickup"),
    ]

    DELIVERY_CHOICES = [
        ("PICKUP", "Pickup"),
        ("DELIVERY", "Delivery"),
    ]

    order_number = models.CharField(max_length=20, unique=True)

    customer_name = models.CharField(max_length=150)

    phone_number = models.CharField(max_length=20)

    email = models.EmailField(blank=True)

    delivery_method = models.CharField(
        max_length=20,
        choices=DELIVERY_CHOICES,
        default="PICKUP",
    )

    delivery_address = models.TextField(
        blank=True,
    )

    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_CHOICES,
    )

    status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES,
        default="PENDING",
    )

    total_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )

    special_instructions = models.TextField(
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    def __str__(self):
        return self.order_number


class OrderItem(models.Model):

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="items",
    )

    menu_item = models.ForeignKey(
        "menu.MenuItem",
        on_delete=models.CASCADE,
    )

    quantity = models.PositiveIntegerField()

    price = models.DecimalField(
        max_digits=8,
        decimal_places=2,
    )

    subtotal = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )

    def __str__(self):
        return f"{self.menu_item.name} x {self.quantity}"

# Create your models here.

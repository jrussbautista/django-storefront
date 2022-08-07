from django.db import models
from django.core.validators import MinValueValidator


class Promotion(models.Model):
    description = models.CharField(max_length=255)
    discount = models.FloatField()


class Collection(models.Model):
    title = models.CharField(max_length=255)
    featured_product = models.ForeignKey(
        "Product", on_delete=models.SET_NULL, null=True, related_name="+"
    )


class Product(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField()
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    inventory = models.IntegerField(validators=[MinValueValidator(1)])
    last_update = models.DateTimeField(auto_now=True)
    collection = models.ForeignKey(
        Collection,
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        related_name="products",
    )
    promotions = models.ManyToManyField(Promotion, related_name="products", blank=True)


class Customer(models.Model):
    MEMBERSHIP_GOLD = "G"
    MEMBERSHIP_SILVER = "S"
    MEMBERSHIP_BRONZE = "B"

    MEMBERSHIP_CHOICES = [
        (MEMBERSHIP_GOLD, "Gold"),
        (MEMBERSHIP_SILVER, "Silver"),
        (MEMBERSHIP_BRONZE, "Bronze"),
    ]

    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=255)
    birth_date = models.DateField(null=True)
    membership = models.CharField(max_length=1, default=MEMBERSHIP_BRONZE)


class Order(models.Model):
    PAYMENT_STATUS_PENDING = "P"
    PAYMENT_STATUS_COMPLETED = "C"
    PAYMENT_STATUS_FAILED = "FAILED"

    PAYMENT_STATUS = [
        (PAYMENT_STATUS_PENDING, "PENDING"),
        (PAYMENT_STATUS_COMPLETED, "COMPLETED"),
        (PAYMENT_STATUS_FAILED, "FAILED"),
    ]

    placed_at = models.DateField(auto_now_add=True)
    payment_status = models.CharField(max_length=1, default=PAYMENT_STATUS_PENDING)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)


class OrderItem(models.Model):
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)
    order = models.ForeignKey(Order, on_delete=models.PROTECT)
    product = models.ForeignKey(
        Product, on_delete=models.PROTECT, related_name="order_items"
    )


class Cart(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)


class CartItem(models.Model):
    cart = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()


class Address(models.Model):
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
    )

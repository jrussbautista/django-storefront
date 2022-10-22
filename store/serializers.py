from dataclasses import fields
from decimal import Decimal
from pyexpat import model
from rest_framework import serializers
from .models import (
    Cart,
    CartItem,
    Collection,
    Customer,
    Order,
    OrderItem,
    Product,
    Review,
)


class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ["id", "title"]


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            "id",
            "title",
            "slug",
            "description",
            "price",
            "price_with_tax",
            "inventory",
            "collection",
        ]

    price_with_tax = serializers.SerializerMethodField(method_name="calculate_tax")

    def calculate_tax(self, product: Product):
        TAX = Decimal(1.1)
        return product.price * TAX


class SimpleProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", "title", "price"]


class UpdateCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ["quantity"]


class AddCartItemSerializer(serializers.ModelSerializer):

    product_id = serializers.IntegerField()

    class Meta:
        model = CartItem
        fields = ["id", "product_id", "quantity"]

    def validate_product_id(self, value):
        if not Product.objects.filter(pk=value).exists():
            raise serializers.ValidationError("No product with the given id was found")
        return value

    def save(self, **kwargs):
        cart_id = self.context["cart_id"]
        product_id = self.validated_data["product_id"]
        quantity = self.validated_data["quantity"]
        try:
            cart_item = CartItem.objects.get(cart_id=cart_id, product_id=product_id)
            cart_item.quantity += quantity
            cart_item.save()
            self.instance = cart_item
        except CartItem.DoesNotExist:
            self.instance = CartItem.objects.create(
                cart_id=cart_id, **self.validated_data
            )
        return self.instance


class CartItemSerializer(serializers.ModelSerializer):
    product = SimpleProductSerializer()
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ["id", "product", "quantity", "total_price"]

    def get_total_price(self, cart_item: CartItem):
        return cart_item.quantity * cart_item.product.price


class CartSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ["id", "items", "total_price"]

    def get_total_price(self, cart):
        return sum([item.quantity * item.product.price for item in cart.items.all()])


class CustomerSerializer(serializers.ModelSerializer):

    user_id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Customer
        fields = ["id", "user_id", "phone", "birth_date", "membership"]


class OrderItemSerializer(serializers.ModelSerializer):

    product = SimpleProductSerializer()

    class Meta:
        model = OrderItem
        fields = ["id", "product", "unit_price", "quantity"]


class OrderSerializer(serializers.ModelSerializer):

    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ["id", "customer", "placed_at", "payment_status", "items"]


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ["id", "date", "name", "description"]

    def create(self, validated_data):
        product_id = self.context["product_id"]
        return Review.objects.create(product_id=product_id, **validated_data)

from decimal import Decimal
from rest_framework import serializers
from .models import Collection, Product


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

from rest_framework import serializers
from .models import Collection, Product


class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ["id", "title"]


class ProductSerializer(serializers.ModelSerializer):

    collection = CollectionSerializer()

    class Meta:
        model = Product
        fields = ["id", "title", "slug", "description", "price", "collection"]

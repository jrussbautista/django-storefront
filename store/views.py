from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from .serializers import ProductSerializer
from .models import Product


class ProductList(APIView):
    def get(self, request):
        query_set = Product.objects.all()
        serializer = ProductSerializer(instance=query_set, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ProductDetail(APIView):
    def get_object(self, pk):
        try:
            return Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return Response(
                data={"detail": "Not found"}, status=status.HTTP_404_NOT_FOUND
            )

    def get(self, request, pk):
        product = self.get_object(pk)
        serializer = ProductSerializer(product)
        return Response(serializer.data)

    def put(self, request, pk):
        product = self.get_object(pk)
        serializer = ProductSerializer(data=request.data, instance=product)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, pk):
        product = self.get_object(pk)
        if product.order_items.count() > 0:
            return Response(
                {"error", "Product cannot be deleted"},
                status=status.HTTP_405_METHOD_NOT_ALLOWED,
            )
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

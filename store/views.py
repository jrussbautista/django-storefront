from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

from .serializers import ProductSerializer
from .models import Product


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.select_related("collection").all()
    serializer_class = ProductSerializer

    def get_serializer_context(self):
        return {"request": self.request}

    def get_object(self, pk):
        try:
            return Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return Response(
                data={"detail": "Not found"}, status=status.HTTP_404_NOT_FOUND
            )

    def delete(self, request, pk):
        product = self.get_object(pk)
        if product.order_items.count() > 0:
            return Response(
                {"error", "Product cannot be deleted"},
                status=status.HTTP_405_METHOD_NOT_ALLOWED,
            )
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

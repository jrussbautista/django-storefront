from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .serializers import ProductSerializer
from .models import Product


@api_view()
def product_list(request):
    query_set = Product.objects.all()
    serializer = ProductSerializer(instance=query_set, many=True)
    return Response(serializer.data)


@api_view()
def product_detail(request, id):
    try:
        product = Product.objects.get(pk=id)
        serializer = ProductSerializer(product)
        return Response(serializer.data)
    except Product.DoesNotExist:
        return Response(data={"detail": "Not found"}, status=status.HTTP_404_NOT_FOUND)

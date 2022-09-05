from django.contrib import admin
from django.urls import path
from rest_framework.routers import SimpleRouter
from . import views


router = SimpleRouter()
router.register("products", views.ProductViewSet, basename="products")
router.register("carts", views.CartViewSet, basename="carts")

urlpatterns = router.urls

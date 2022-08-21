from django.contrib import admin
from django.urls import path
from rest_framework.routers import SimpleRouter
from . import views


router = SimpleRouter()
router.register("products", views.ProductViewSet, basename="products")

urlpatterns = router.urls

from rest_framework_nested import routers
from . import views


router = routers.DefaultRouter()
router.register("products", views.ProductViewSet, basename="products")
router.register("carts", views.CartViewSet, basename="carts")
router.register("customers", views.CustomerViewSet)
router.register("orders", views.OrderViewSet)

cart_routers = routers.NestedDefaultRouter(router, "carts", lookup="cart")
cart_routers.register("items", views.CartItemViewSet, basename="cart-items")

urlpatterns = router.urls + cart_routers.urls

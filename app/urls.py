from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from products.api import (
    CustomersViewset,
    AddressesViewset,
    CategoriesViewset,
    ManufacturersViewset,
    ProductsViewset,
    ProductPhotosViewset,
    OrdersViewset,
    OrderItemsViewset,
    ReviewsViewset,
    ProfileViewSet,
)

router = DefaultRouter()
router.register("customers", CustomersViewset, "customers")
router.register("addresses", AddressesViewset, "addresses")
router.register("categories", CategoriesViewset, "categories")
router.register("manufacturers", ManufacturersViewset, "manufacturers")
router.register("products", ProductsViewset, "products")
router.register("product-photos", ProductPhotosViewset, "product-photos")
router.register("orders", OrdersViewset, "orders")
router.register("order-items", OrderItemsViewset, "order-items")
router.register("reviews", ReviewsViewset, "reviews")
router.register("profile", ProfileViewSet, "profile")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
] + static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT
)
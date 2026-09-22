from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from rest_framework.routers import DefaultRouter
from products.api import CategoryViewSet, ProductViewSet, OrderViewSet, OrderItemViewSet, ReviewViewSet

router = DefaultRouter()
router.register('categories', CategoryViewSet)
router.register('products', ProductViewSet)
router.register('orders', OrderViewSet)
router.register('order-items', OrderItemViewSet)
router.register('reviews', ReviewViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('', RedirectView.as_view(url='/api/')),
]
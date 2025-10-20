from __future__ import annotations

from rest_framework.routers import DefaultRouter

from .views import (
    AppointmentViewSet,
    OrderViewSet,
    PriceRuleViewSet,
    ProviderViewSet,
    PublicProductViewSet,
    PublicServiceViewSet,
)

router = DefaultRouter()
router.register("services", PublicServiceViewSet, basename="service")
router.register("products", PublicProductViewSet, basename="product")
router.register("appointments", AppointmentViewSet, basename="appointment")
router.register("orders", OrderViewSet, basename="order")
router.register("price-rules", PriceRuleViewSet, basename="price-rule")
router.register("providers", ProviderViewSet, basename="provider")

urlpatterns = router.urls

from __future__ import annotations

from django.urls import include, path
from django.views.generic import TemplateView

urlpatterns = [
    path("", TemplateView.as_view(template_name="backoffice/index.html"), name="index"),
    path("services/", include(("apps.catalog.back_urls", "catalog"), namespace="catalog")),
    path("products/", include(("apps.catalog.product_back_urls", "products"), namespace="products")),
    path("providers/", include(("apps.people.back_urls", "providers"), namespace="providers")),
    path("pricing/", include(("apps.pricing.back_urls", "pricing"), namespace="pricing")),
    path("orders/", include(("apps.orders.back_urls", "orders"), namespace="orders")),
    path("booking/", include(("apps.booking.back_urls", "booking"), namespace="booking")),
]

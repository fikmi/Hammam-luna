from __future__ import annotations

from rest_framework import permissions, viewsets

from apps.booking.models import Appointment
from apps.catalog.models import Product, Service
from apps.orders.models import Order
from apps.people.models import Provider
from apps.pricing.models import PriceRule

from .serializers import (
    AppointmentSerializer,
    OrderSerializer,
    PriceRuleSerializer,
    ProductSerializer,
    ProviderSerializer,
    ServiceSerializer,
)


class PublicServiceViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Service.objects.filter(is_active=True)
    serializer_class = ServiceSerializer
    permission_classes = [permissions.AllowAny]
    filterset_fields = ("is_active",)
    search_fields = ("name", "description")
    ordering_fields = ("name", "base_price")


class PublicProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.filter(is_active=True)
    serializer_class = ProductSerializer
    permission_classes = [permissions.AllowAny]
    filterset_fields = ("is_active",)
    search_fields = ("name", "description", "sku")
    ordering_fields = ("name", "price")


class AuthenticatedViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]


class AppointmentViewSet(AuthenticatedViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    filterset_fields = ("status", "provider", "service", "customer")
    ordering_fields = ("start_at",)


class OrderViewSet(AuthenticatedViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    filterset_fields = ("status", "customer")
    ordering_fields = ("created_at",)


class ProviderViewSet(AuthenticatedViewSet):
    queryset = Provider.objects.all()
    serializer_class = ProviderSerializer
    filterset_fields = ("is_active",)
    search_fields = ("name", "skills")


class PriceRuleViewSet(AuthenticatedViewSet):
    queryset = PriceRule.objects.all()
    serializer_class = PriceRuleSerializer
    filterset_fields = ("applies_to", "target_id", "rule_type")

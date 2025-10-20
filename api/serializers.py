from __future__ import annotations

from rest_framework import serializers

from apps.booking.models import Appointment
from apps.catalog.models import Product, Service
from apps.orders.models import Order, OrderItem
from apps.people.models import Provider
from apps.pricing.models import PriceRule


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ("id", "name", "description", "duration_min", "base_price", "is_active")


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ("id", "sku", "name", "description", "price", "stock_qty", "is_active")


class ProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Provider
        fields = ("id", "name", "contact_email", "phone", "skills", "rating", "is_active")


class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = (
            "id",
            "customer",
            "service",
            "provider",
            "start_at",
            "end_at",
            "status",
            "notes",
        )


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ("id", "kind", "ref_id", "name", "qty", "unit_price", "total")


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ("id", "customer", "status", "total", "currency", "items", "created_at")


class PriceRuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = PriceRule
        fields = ("id", "name", "applies_to", "target_id", "rule_type", "value", "start_at", "end_at")

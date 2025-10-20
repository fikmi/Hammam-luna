from __future__ import annotations

from django.contrib import admin

from .models import Product, Service


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("name", "duration_min", "base_price", "is_active")
    search_fields = ("name",)
    list_filter = ("is_active",)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("sku", "name", "price", "stock_qty", "is_active")
    search_fields = ("sku", "name")
    list_filter = ("is_active",)

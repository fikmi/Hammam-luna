from __future__ import annotations

from django import forms

from .models import Product, Service


class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ("name", "description", "duration_min", "base_price", "is_active", "provider")


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ("sku", "name", "description", "price", "stock_qty", "is_active")

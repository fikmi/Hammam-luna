from __future__ import annotations

from django.contrib import admin

from .models import PriceRule


@admin.register(PriceRule)
class PriceRuleAdmin(admin.ModelAdmin):
    list_display = ("name", "applies_to", "target_id", "rule_type", "start_at", "end_at")
    list_filter = ("applies_to", "rule_type")
    search_fields = ("name",)

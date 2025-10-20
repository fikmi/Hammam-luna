from __future__ import annotations

from django import forms

from .models import PriceRule


class PriceRuleForm(forms.ModelForm):
    class Meta:
        model = PriceRule
        fields = ("name", "applies_to", "target_id", "rule_type", "value", "start_at", "end_at")
        widgets = {
            "start_at": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "end_at": forms.DateTimeInput(attrs={"type": "datetime-local"}),
        }

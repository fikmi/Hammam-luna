from __future__ import annotations

from django import forms

from .models import Customer


class CustomerProfileForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = (
            "first_name",
            "last_name",
            "email",
            "phone",
            "default_address",
            "notes",
        )

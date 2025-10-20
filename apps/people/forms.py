from __future__ import annotations

from django import forms

from .models import Provider


class ProviderForm(forms.ModelForm):
    class Meta:
        model = Provider
        fields = ("name", "contact_email", "phone", "skills", "rating", "is_active")
        widgets = {"skills": forms.Textarea(attrs={"rows": 2})}

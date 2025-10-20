from __future__ import annotations

from django import forms
from django.utils import timezone

from apps.people.models import Provider

from .models import Appointment


class AppointmentForm(forms.Form):
    provider = forms.ModelChoiceField(queryset=Provider.objects.filter(is_active=True))
    start_at = forms.DateTimeField(widget=forms.DateTimeInput(attrs={"type": "datetime-local"}))
    notes = forms.CharField(widget=forms.Textarea, required=False)

    def __init__(self, service, customer, *args, **kwargs):
        self.service = service
        self.customer = customer
        super().__init__(*args, **kwargs)
        self.fields["provider"].queryset = service.available_providers()

    def clean_start_at(self):
        start_at = self.cleaned_data["start_at"]
        if start_at < timezone.now():
            raise forms.ValidationError("Choisir un créneau futur")
        return start_at

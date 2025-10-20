from __future__ import annotations

from django import forms

from .models import Payment


class CheckoutForm(forms.Form):
    payment_method = forms.ChoiceField(choices=Payment.Method.choices)

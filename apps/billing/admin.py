from __future__ import annotations

from django.contrib import admin

from .models import CreditNote, Invoice


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ("order", "total", "currency", "created_at")


@admin.register(CreditNote)
class CreditNoteAdmin(admin.ModelAdmin):
    list_display = ("order", "amount", "created_at")

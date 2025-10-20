from __future__ import annotations

from django.contrib import admin

from .models import Appointment


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ("service", "provider", "customer", "start_at", "status")
    list_filter = ("status", "provider")
    search_fields = ("service__name", "customer__first_name", "customer__last_name")

from __future__ import annotations

from django.contrib import admin

from .models import Provider, ProviderAvailability, ProviderTimeOff, Staff


@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ("user", "role", "is_active", "created_at")
    list_filter = ("role", "is_active")
    search_fields = ("user__username", "user__email")


class AvailabilityInline(admin.TabularInline):
    model = ProviderAvailability
    extra = 1


class TimeOffInline(admin.TabularInline):
    model = ProviderTimeOff
    extra = 0


@admin.register(Provider)
class ProviderAdmin(admin.ModelAdmin):
    list_display = ("name", "contact_email", "phone", "rating", "is_active")
    list_filter = ("is_active",)
    search_fields = ("name", "contact_email")
    inlines = [AvailabilityInline, TimeOffInline]


admin.site.register(ProviderAvailability)
admin.site.register(ProviderTimeOff)

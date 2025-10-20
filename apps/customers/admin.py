from __future__ import annotations

from django.contrib import admin

from .models import Collaborator, Customer


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "email", "phone", "created_at")
    search_fields = ("first_name", "last_name", "email")


@admin.register(Collaborator)
class CollaboratorAdmin(admin.ModelAdmin):
    list_display = ("user", "role_label", "hourly_cost", "is_active")
    list_filter = ("is_active",)
    search_fields = ("user__username", "role_label")

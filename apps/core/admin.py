from __future__ import annotations

from django.contrib import admin

from .models import AuditLog, SiteSetting, TwoFactorProfile


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ("action", "entity", "entity_id", "actor", "at")
    list_filter = ("action", "entity")
    search_fields = ("action", "entity", "entity_id", "actor__username")


@admin.register(SiteSetting)
class SiteSettingAdmin(admin.ModelAdmin):
    list_display = ("key", "created_at", "updated_at")
    search_fields = ("key",)


@admin.register(TwoFactorProfile)
class TwoFactorProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "enabled", "updated_at")
    list_filter = ("enabled",)
    search_fields = ("user__username", "user__email")

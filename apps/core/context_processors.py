from __future__ import annotations

from django.conf import settings


def settings_context(_request):
    return {
        "TWO_FACTOR_ENABLED": settings.TWO_FACTOR_ENABLED,
        "SITE_NAME": "Hammam Luna",
    }

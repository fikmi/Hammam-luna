from __future__ import annotations

import json
from typing import Any

from django.contrib.auth.models import AnonymousUser
from django.http import HttpRequest, HttpResponse

from .models import AuditLog


class AuditLogMiddleware:
    """Persist audit information for mutating requests."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        response = self.get_response(request)
        if request.method in {"POST", "PUT", "PATCH", "DELETE"} and response.status_code < 400:
            user = request.user if not isinstance(request.user, AnonymousUser) else None
            AuditLog.objects.create(
                actor=user,
                action=f"{request.method} {request.path}",
                entity=request.resolver_match.view_name if request.resolver_match else request.path,
                entity_id=str(getattr(getattr(response, "context_data", None), "id", request.POST.get("id", "-"))),
                payload=self._build_payload(request),
            )
        return response

    def _build_payload(self, request: HttpRequest) -> dict[str, Any]:
        if request.content_type == "application/json" and request.body:
            try:
                return json.loads(request.body.decode())
            except json.JSONDecodeError:  # pragma: no cover - safety net
                return {"body": request.body.decode(errors="ignore")}
        return request.POST.dict()

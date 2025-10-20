from __future__ import annotations

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin


class BackOfficePermissionRequired(LoginRequiredMixin, PermissionRequiredMixin):
    raise_exception = True
    permission_required = ""

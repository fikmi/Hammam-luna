from __future__ import annotations

from django.urls import path

from . import back_views

urlpatterns = [
    path("", back_views.AppointmentCalendarView.as_view(), name="calendar"),
    path("<int:pk>/", back_views.AppointmentUpdateView.as_view(), name="update"),
]

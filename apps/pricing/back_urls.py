from __future__ import annotations

from django.urls import path

from . import back_views

urlpatterns = [
    path("", back_views.PriceRuleListView.as_view(), name="list"),
    path("new/", back_views.PriceRuleCreateView.as_view(), name="create"),
    path("<int:pk>/", back_views.PriceRuleUpdateView.as_view(), name="update"),
]

from __future__ import annotations

import pytest
from django.utils import timezone

from apps.pricing.models import PriceRule
from apps.pricing.services import PricingEngine
from factories import PriceRuleFactory, ProductFactory, ServiceFactory


@pytest.mark.django_db
def test_percentage_price_rule_service():
    service = ServiceFactory(base_price=100)
    rule = PriceRuleFactory(bind_service=service, value=20)
    engine = PricingEngine()
    assert engine.for_service(service) == pytest.approx(80)


@pytest.mark.django_db
def test_fixed_rule_product():
    product = ProductFactory(price=50)
    PriceRule.objects.create(
        name="Promo",
        applies_to=PriceRule.AppliesTo.PRODUCT,
        target_id=product.pk,
        rule_type=PriceRule.RuleType.FIXED,
        value=40,
        start_at=timezone.now() - timezone.timedelta(days=1),
        end_at=timezone.now() + timezone.timedelta(days=1),
    )
    engine = PricingEngine()
    assert engine.for_product(product) == pytest.approx(40)

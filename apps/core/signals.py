from __future__ import annotations

from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import TwoFactorProfile
from .otp import random_base32

User = get_user_model()


@receiver(post_save, sender=User)
def ensure_two_factor(sender, instance: User, created: bool, **_: object) -> None:
    if created:
        TwoFactorProfile.objects.get_or_create(user=instance, defaults={"secret": random_base32()})
    else:
        TwoFactorProfile.objects.get_or_create(user=instance, defaults={"secret": random_base32()})

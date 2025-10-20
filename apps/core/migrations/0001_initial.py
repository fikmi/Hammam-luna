from __future__ import annotations

from django.conf import settings
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="AuditLog",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("action", models.CharField(max_length=255)),
                ("entity", models.CharField(max_length=255)),
                ("entity_id", models.CharField(max_length=255)),
                ("payload", models.JSONField(blank=True, default=dict)),
                ("at", models.DateTimeField(default=django.utils.timezone.now)),
                ("actor", models.ForeignKey(blank=True, null=True, on_delete=models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={"ordering": ["-at"]},
        ),
        migrations.CreateModel(
            name="SiteSetting",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("key", models.CharField(max_length=255, unique=True)),
                ("value", models.JSONField(blank=True, default=dict)),
            ],
            options={"verbose_name": "Paramètre", "verbose_name_plural": "Paramètres"},
        ),
        migrations.CreateModel(
            name="TwoFactorProfile",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("secret", models.CharField(blank=True, max_length=32)),
                ("enabled", models.BooleanField(default=False)),
                ("user", models.OneToOneField(on_delete=models.deletion.CASCADE, related_name="two_factor", to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

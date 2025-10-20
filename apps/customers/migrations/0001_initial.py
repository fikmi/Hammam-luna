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
            name="Customer",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("first_name", models.CharField(max_length=120)),
                ("last_name", models.CharField(blank=True, max_length=120)),
                ("email", models.EmailField(max_length=254, unique=True)),
                ("phone", models.CharField(blank=True, max_length=30)),
                ("default_address", models.TextField(blank=True)),
                ("notes", models.TextField(blank=True)),
                (
                    "user",
                    models.OneToOneField(blank=True, null=True, on_delete=models.deletion.SET_NULL, related_name="customer", to=settings.AUTH_USER_MODEL),
                ),
            ],
            options={"ordering": ["first_name", "last_name"]},
        ),
        migrations.CreateModel(
            name="Collaborator",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("role_label", models.CharField(max_length=120)),
                ("hourly_cost", models.DecimalField(decimal_places=2, max_digits=8)),
                ("is_active", models.BooleanField(default=True)),
                (
                    "user",
                    models.ForeignKey(on_delete=models.deletion.CASCADE, related_name="collaborations", to=settings.AUTH_USER_MODEL),
                ),
            ],
        ),
    ]

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
            name="Provider",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("name", models.CharField(max_length=255)),
                ("contact_email", models.EmailField(max_length=254)),
                ("phone", models.CharField(blank=True, max_length=30)),
                ("skills", models.JSONField(blank=True, default=list)),
                ("rating", models.DecimalField(decimal_places=2, max_digits=3, default=0)),
                ("is_active", models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name="Staff",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("role", models.CharField(choices=[("OWNER", "Propriétaire"), ("STAFF", "Equipe")], max_length=20)),
                ("is_active", models.BooleanField(default=True)),
                (
                    "user",
                    models.OneToOneField(on_delete=models.deletion.CASCADE, related_name="staff_profile", to=settings.AUTH_USER_MODEL),
                ),
            ],
        ),
        migrations.CreateModel(
            name="ProviderAvailability",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("weekday", models.IntegerField(help_text="0=lundi")),
                ("start_hour", models.TimeField()),
                ("end_hour", models.TimeField()),
                (
                    "provider",
                    models.ForeignKey(on_delete=models.deletion.CASCADE, related_name="availabilities", to="people.provider"),
                ),
            ],
            options={"ordering": ["provider", "weekday", "start_hour"], "verbose_name": "Disponibilité", "verbose_name_plural": "Disponibilités"},
        ),
        migrations.CreateModel(
            name="ProviderTimeOff",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("start_at", models.DateTimeField()),
                ("end_at", models.DateTimeField()),
                ("reason", models.CharField(blank=True, max_length=255)),
                (
                    "provider",
                    models.ForeignKey(on_delete=models.deletion.CASCADE, related_name="exclusions", to="people.provider"),
                ),
            ],
            options={"ordering": ["-start_at"], "verbose_name": "Indisponibilité", "verbose_name_plural": "Indisponibilités"},
        ),
    ]

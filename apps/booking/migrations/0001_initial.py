from __future__ import annotations

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("customers", "0001_initial"),
        ("catalog", "0001_initial"),
        ("people", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Appointment",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("start_at", models.DateTimeField()),
                ("end_at", models.DateTimeField()),
                ("status", models.CharField(choices=[("pending", "En attente"), ("confirmed", "Confirmé"), ("done", "Terminé"), ("no_show", "Absent"), ("canceled", "Annulé")], default="pending", max_length=20)),
                ("notes", models.TextField(blank=True)),
                ("customer", models.ForeignKey(on_delete=models.deletion.CASCADE, related_name="appointments", to="customers.customer")),
                ("provider", models.ForeignKey(on_delete=models.deletion.CASCADE, related_name="appointments", to="people.provider")),
                ("service", models.ForeignKey(on_delete=models.deletion.CASCADE, related_name="appointments", to="catalog.service")),
            ],
            options={"ordering": ["-start_at"], "unique_together": {("provider", "start_at")}},
        ),
    ]

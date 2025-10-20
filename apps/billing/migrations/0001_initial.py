from __future__ import annotations

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("orders", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Invoice",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("pdf", models.FileField(upload_to="invoices/")),
                ("total", models.DecimalField(decimal_places=2, max_digits=10)),
                ("currency", models.CharField(default="EUR", max_length=10)),
                ("order", models.OneToOneField(on_delete=models.deletion.CASCADE, related_name="invoice", to="orders.order")),
            ],
        ),
        migrations.CreateModel(
            name="CreditNote",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("pdf", models.FileField(upload_to="credit_notes/")),
                ("amount", models.DecimalField(decimal_places=2, max_digits=10)),
                ("order", models.OneToOneField(on_delete=models.deletion.CASCADE, related_name="credit_note", to="orders.order")),
            ],
        ),
    ]

from __future__ import annotations

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="PriceRule",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("name", models.CharField(max_length=255)),
                ("applies_to", models.CharField(choices=[("service", "Service"), ("product", "Produit")], max_length=20)),
                ("target_id", models.PositiveIntegerField()),
                ("rule_type", models.CharField(choices=[("fixed", "Montant fixe"), ("percent", "Pourcentage"), ("tier", "Palier")], max_length=20)),
                ("value", models.JSONField()),
                ("start_at", models.DateTimeField()),
                ("end_at", models.DateTimeField(blank=True, null=True)),
            ],
            options={"ordering": ["name"]},
        ),
    ]

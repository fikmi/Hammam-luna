from __future__ import annotations

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("customers", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Order",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("status", models.CharField(choices=[("cart", "Panier"), ("pending", "En attente"), ("paid", "Payée"), ("shipped", "Expédiée"), ("completed", "Terminée"), ("canceled", "Annulée")], default="cart", max_length=20)),
                ("total", models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ("currency", models.CharField(default="EUR", max_length=10)),
                ("customer", models.ForeignKey(on_delete=models.deletion.CASCADE, related_name="orders", to="customers.customer")),
            ],
            options={"ordering": ["-created_at"]},
        ),
        migrations.CreateModel(
            name="OrderItem",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("kind", models.CharField(choices=[("service", "Service"), ("product", "Produit")], max_length=20)),
                ("ref_id", models.PositiveIntegerField()),
                ("name", models.CharField(max_length=255)),
                ("qty", models.PositiveIntegerField(default=1)),
                ("unit_price", models.DecimalField(decimal_places=2, max_digits=8)),
                ("total", models.DecimalField(decimal_places=2, max_digits=10)),
                ("order", models.ForeignKey(on_delete=models.deletion.CASCADE, related_name="items", to="orders.order")),
            ],
            options={"ordering": ["order", "pk"]},
        ),
        migrations.CreateModel(
            name="Payment",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("method", models.CharField(choices=[("card", "Carte"), ("cash", "Espèces"), ("transfer", "Virement")], max_length=20)),
                ("amount", models.DecimalField(decimal_places=2, max_digits=10)),
                ("status", models.CharField(choices=[("authorized", "Autorisé"), ("captured", "Capturé"), ("failed", "Echoué"), ("refunded", "Remboursé")], max_length=20)),
                ("txn_ref", models.CharField(blank=True, max_length=255)),
                ("paid_at", models.DateTimeField(blank=True, null=True)),
                ("order", models.ForeignKey(on_delete=models.deletion.CASCADE, related_name="payments", to="orders.order")),
            ],
        ),
    ]

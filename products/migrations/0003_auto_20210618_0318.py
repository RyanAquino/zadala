# Generated by Django 3.0.8 on 2021-06-18 03:18

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("products", "0002_auto_20210324_0315"),
    ]

    operations = [
        migrations.AlterField(
            model_name="product",
            name="price",
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=20),
        ),
    ]

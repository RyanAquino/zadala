# Generated by Django 3.2.12 on 2022-03-29 01:52

import django.contrib.postgres.indexes
import django.db.models.functions.text
from django.contrib.postgres.operations import BtreeGinExtension, TrigramExtension
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("products", "0003_auto_20210618_0318"),
    ]

    operations = [
        BtreeGinExtension(),
        TrigramExtension(),
        migrations.AddIndex(
            model_name="product",
            index=django.contrib.postgres.indexes.GinIndex(
                django.contrib.postgres.indexes.OpClass(
                    django.db.models.functions.text.Upper("name"), name="gin_trgm_ops"
                ),
                name="products_name_gin_index",
            ),
        ),
    ]
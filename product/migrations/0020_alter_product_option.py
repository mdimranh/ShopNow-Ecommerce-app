# Generated by Django 4.0.1 on 2022-02-17 05:56

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0019_alter_product_option'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='option',
            field=django.contrib.postgres.fields.ArrayField(base_field=django.contrib.postgres.fields.ArrayField(base_field=models.TextField(blank=True, null=True), size=None), blank=True, null=True, size=None),
        ),
    ]

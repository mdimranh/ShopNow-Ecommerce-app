# Generated by Django 4.0.1 on 2022-03-30 03:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0004_options_style'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='option',
            field=models.ManyToManyField(blank=True, related_name='options', to='product.Options'),
        ),
    ]

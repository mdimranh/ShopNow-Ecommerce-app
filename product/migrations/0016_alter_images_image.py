# Generated by Django 4.0.1 on 2022-02-16 03:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0015_remove_product_hot_deal_product_hot_deal_discount_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='images',
            name='image',
            field=models.TextField(blank=True),
        ),
    ]
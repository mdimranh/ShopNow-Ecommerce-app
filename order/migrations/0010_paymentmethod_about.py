# Generated by Django 4.0.1 on 2022-04-21 05:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0009_cart_color_cart_size_remove_cart_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='paymentmethod',
            name='about',
            field=models.TextField(blank=True, null=True),
        ),
    ]

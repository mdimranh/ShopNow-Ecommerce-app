# Generated by Django 4.0 on 2021-12-17 05:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0004_rename_exclude_categories_userrestrictions_exclude categories_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='shopcart',
            name='coupon',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='order.coupon'),
        ),
    ]

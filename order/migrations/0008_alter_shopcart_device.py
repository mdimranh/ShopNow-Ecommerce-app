# Generated by Django 4.0.1 on 2022-04-18 10:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0007_shopcart_device_alter_shopcart_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shopcart',
            name='device',
            field=models.TextField(blank=True, null=True),
        ),
    ]

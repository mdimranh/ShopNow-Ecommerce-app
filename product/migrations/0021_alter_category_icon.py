# Generated by Django 4.0.1 on 2022-02-23 15:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0020_alter_product_option'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='icon',
            field=models.CharField(max_length=100),
        ),
    ]
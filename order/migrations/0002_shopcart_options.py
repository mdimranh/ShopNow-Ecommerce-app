# Generated by Django 4.0.1 on 2022-03-30 03:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='shopcart',
            name='options',
            field=models.TextField(blank=True, null=True),
        ),
    ]

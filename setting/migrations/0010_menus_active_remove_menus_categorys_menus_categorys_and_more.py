# Generated by Django 4.0.1 on 2022-02-20 10:27

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('setting', '0009_menus_icon'),
    ]

    operations = [
        migrations.AddField(
            model_name='menus',
            name='active',
            field=models.BooleanField(default=True),
        ),
        migrations.RemoveField(
            model_name='menus',
            name='categorys',
        ),
        migrations.AddField(
            model_name='menus',
            name='categorys',
            field=django.contrib.postgres.fields.ArrayField(base_field=django.contrib.postgres.fields.ArrayField(base_field=models.TextField(blank=True, null=True), size=None), blank=True, null=True, size=None),
        ),
        migrations.RemoveField(
            model_name='menus',
            name='groups',
        ),
        migrations.AddField(
            model_name='menus',
            name='groups',
            field=django.contrib.postgres.fields.ArrayField(base_field=django.contrib.postgres.fields.ArrayField(base_field=models.TextField(blank=True, null=True), size=None), blank=True, null=True, size=None),
        ),
    ]

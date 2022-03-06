# Generated by Django 4.0.1 on 2022-03-06 16:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('region', '0004_alter_area_city_alter_city_region_and_more'),
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='addressbook',
            name='area',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='region.area'),
        ),
        migrations.AlterField(
            model_name='addressbook',
            name='city',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='region.city'),
        ),
        migrations.AlterField(
            model_name='addressbook',
            name='country',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='region.country'),
        ),
        migrations.AlterField(
            model_name='addressbook',
            name='region',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='region.region'),
        ),
    ]

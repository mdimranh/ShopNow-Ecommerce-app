# Generated by Django 4.0 on 2021-12-29 10:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('setting', '0011_siteconfiguration_site_logo_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='siteconfiguration',
            name='site_logo',
            field=models.ImageField(default='/settings/logo.png', upload_to='settings/'),
        ),
    ]

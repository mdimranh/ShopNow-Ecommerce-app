# Generated by Django 4.0 on 2021-12-31 05:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('setting', '0016_alter_slidersetting_slider'),
    ]

    operations = [
        migrations.AddField(
            model_name='slidersetting',
            name='autoplay_timeout',
            field=models.IntegerField(default=4000),
        ),
    ]

# Generated by Django 4.0 on 2021-12-31 18:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('setting', '0021_alter_slidersetting_slider'),
    ]

    operations = [
        migrations.AddField(
            model_name='slider',
            name='arrows',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='slider',
            name='autoplay',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='slider',
            name='autoplay_timeout',
            field=models.IntegerField(default=4000),
        ),
        migrations.DeleteModel(
            name='SliderSetting',
        ),
    ]

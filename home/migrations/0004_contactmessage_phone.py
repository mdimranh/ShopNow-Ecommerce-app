# Generated by Django 4.0.1 on 2022-03-03 15:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_searchkeyword_updated_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='contactmessage',
            name='phone',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]

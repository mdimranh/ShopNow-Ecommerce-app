# Generated by Django 4.0.1 on 2022-03-05 11:15

import ckeditor_uploader.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('setting', '0016_menus_position'),
    ]

    operations = [
        migrations.CreateModel(
            name='Pages',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=500)),
                ('body', ckeditor_uploader.fields.RichTextUploadingField()),
                ('active', models.BooleanField(default=True)),
            ],
        ),
    ]

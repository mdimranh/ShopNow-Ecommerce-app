# Generated by Django 3.2.3 on 2021-12-12 10:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0005_category_group'),
    ]

    operations = [
        migrations.RenameField(
            model_name='category',
            old_name='group',
            new_name='Subcategory_group',
        ),
    ]

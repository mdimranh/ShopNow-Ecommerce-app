# Generated by Django 4.0.1 on 2022-03-17 11:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0015_rename_total_bst_order_total_bdt'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='shopcarts',
        ),
    ]

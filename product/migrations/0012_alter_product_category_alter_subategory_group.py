# Generated by Django 4.0 on 2021-12-21 04:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0011_group_alter_category_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.group'),
        ),
        migrations.AlterField(
            model_name='subategory',
            name='group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='subcategorys', to='product.group'),
        ),
    ]

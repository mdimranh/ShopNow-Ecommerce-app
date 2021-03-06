# Generated by Django 4.0.1 on 2022-03-26 14:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0002_option_remove_product_option_product_option'),
    ]

    operations = [
        migrations.CreateModel(
            name='Options',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('option', models.ManyToManyField(related_name='option', to='product.Option')),
            ],
        ),
        migrations.AlterField(
            model_name='product',
            name='option',
            field=models.ManyToManyField(blank=True, null=True, related_name='options', to='product.Options'),
        ),
    ]

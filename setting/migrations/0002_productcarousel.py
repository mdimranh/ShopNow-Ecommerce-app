# Generated by Django 4.0 on 2022-01-25 02:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0001_initial'),
        ('setting', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductCarousel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('Enable Carousel', models.BooleanField(default=True)),
                ('categories', models.ManyToManyField(to='product.Category')),
            ],
        ),
    ]
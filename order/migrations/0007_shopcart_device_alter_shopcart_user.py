# Generated by Django 4.0.1 on 2022-04-18 10:31

from django.conf import settings
import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('order', '0006_remove_shopcart_coupon_shopcart_coupon'),
    ]

    operations = [
        migrations.AddField(
            model_name='shopcart',
            name='device',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=100, null=True), default=list, size=None),
        ),
        migrations.AlterField(
            model_name='shopcart',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='user_shopcart', to=settings.AUTH_USER_MODEL),
        ),
    ]
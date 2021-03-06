# Generated by Django 4.0.1 on 2022-03-24 10:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Coupon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('code', models.CharField(max_length=50)),
                ('discount_type', models.CharField(choices=[('Fixed', 'Fixed'), ('Percent', 'Percent')], default='Percent', max_length=20)),
                ('value', models.IntegerField()),
                ('free_shipping', models.BooleanField()),
                ('start_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('end_date', models.DateTimeField()),
                ('min_spend', models.FloatField(blank=True, null=True)),
                ('max_spend', models.FloatField(blank=True, null=True)),
                ('limit_per_coupon', models.IntegerField(blank=True, null=True)),
                ('limit_per_customer', models.IntegerField(blank=True, null=True)),
                ('active', models.BooleanField(default=True)),
                ('categories', models.ManyToManyField(related_name='categories', to='product.Category')),
                ('exclude_categories', models.ManyToManyField(related_name='exclude_categories', to='product.Category')),
                ('exclude_products', models.ManyToManyField(related_name='exclude_products', to='product.Product')),
                ('products', models.ManyToManyField(related_name='products', to='product.Product')),
            ],
        ),
        migrations.CreateModel(
            name='PaymentMethod',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('client_id', models.TextField()),
                ('secret', models.TextField()),
                ('active', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='ShippingMethod',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('fee', models.IntegerField()),
                ('method_type', models.CharField(blank=True, max_length=100, null=True)),
                ('active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Wishlist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pro_wishlist', to='product.product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='wishlist', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserRestrictions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('min_spend', models.IntegerField(blank=True, null=True)),
                ('max_spend', models.IntegerField(blank=True, null=True)),
                ('Exclude Categories', models.ManyToManyField(blank=True, related_name='coupon_exclude_categories', to='product.Category')),
                ('Exclude Products', models.ManyToManyField(blank=True, related_name='coupon_exclude_products', to='product.Product')),
                ('categories', models.ManyToManyField(blank=True, related_name='coupon_categories', to='product.Category')),
                ('coupon', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='order.coupon')),
                ('products', models.ManyToManyField(blank=True, related_name='coupon_products', to='product.Product')),
            ],
            options={
                'verbose_name': 'User Restriction',
            },
        ),
        migrations.CreateModel(
            name='UserLimits',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('limit_per_coupon', models.IntegerField(blank=True, null=True)),
                ('limit_per_customer', models.IntegerField(blank=True, null=True)),
                ('coupon', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='order.coupon')),
            ],
            options={
                'verbose_name': 'User Limit',
            },
        ),
        migrations.CreateModel(
            name='ShopCart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=1)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('order_id', models.CharField(blank=True, max_length=500, null=True)),
                ('on_order', models.BooleanField(default=False)),
                ('coupon', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='order.coupon')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_shopcart', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_id', models.TextField(blank=True, null=True)),
                ('payment_mode', models.CharField(blank=True, max_length=200, null=True)),
                ('company_name', models.CharField(blank=True, max_length=500, null=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('notes', models.TextField(blank=True, null=True)),
                ('phone', models.CharField(blank=True, max_length=20, null=True)),
                ('country', models.CharField(blank=True, max_length=100, null=True)),
                ('region', models.CharField(blank=True, max_length=100, null=True)),
                ('city', models.CharField(blank=True, max_length=100, null=True)),
                ('area', models.CharField(blank=True, max_length=300, null=True)),
                ('address', models.CharField(blank=True, max_length=300, null=True)),
                ('shipping_fee', models.CharField(blank=True, max_length=5, null=True)),
                ('total', models.FloatField(blank=True, null=True)),
                ('rate', models.FloatField(blank=True, null=True)),
                ('total_bdt', models.FloatField(blank=True, null=True)),
                ('order_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('status', models.CharField(choices=[('processing', 'Processing'), ('canceled', 'Canceled'), ('completed', 'Completed'), ('pending', 'Pending'), ('pending_payment', 'Pending Payment')], default='processing', max_length=200)),
                ('update', models.DateTimeField(default=django.utils.timezone.now)),
                ('shipping_method', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='order.shippingmethod')),
                ('shopcarts', models.ManyToManyField(to='order.ShopCart')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_order', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

from django.db import models
from product.models import Product
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe

from django.utils.timezone import now

from product.models import Product, Category

DIS_TYPE = (
    ('Fixed', 'Fixed'),
    ('Percent', 'Percent')
)

class Coupon(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=50)
    discount_type = models.CharField(max_length=20, default="Percent", choices=DIS_TYPE)
    value = models.IntegerField()
    free_shipping = models.BooleanField(name='Allow free shipping')
    start_date = models.DateTimeField(default=now)
    end_date = models.DateTimeField()
    active = models.BooleanField()

    def __str__(self):
        return self.name

class UserRestrictions(models.Model):
    coupon = models.ForeignKey(Coupon, on_delete = models.CASCADE)
    min_spend = models.IntegerField(blank=True, null=True)
    max_spend = models.IntegerField(blank=True, null=True)
    products = models.ManyToManyField(Product, blank=True, related_name = 'coupon_products')
    exclude_products = models.ManyToManyField(Product, blank=True, related_name = 'coupon_exclude_products', name='Exclude Products')
    categories = models.ManyToManyField(Category, blank=True, related_name='coupon_categories')
    exclude_categories = models.ManyToManyField(Category, blank=True, related_name='coupon_exclude_categories', name='Exclude Categories')

    def __str__(self):
        return self.coupon.name

    class Meta:
        verbose_name = "User Restriction"

class UserLimits(models.Model):
    coupon = models.ForeignKey(Coupon, on_delete = models.CASCADE)
    limit_per_coupon = models.IntegerField(blank=True, null=True)
    limit_per_customer = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.coupon.name

    class Meta:
        verbose_name = "User Limit"


class ShopCart(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    coupon = models.ForeignKey(Coupon, blank=True, null=True, on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return self.user.first_name+''+self.user.last_name

    def cost(self):
        return (self.product.main_price - (self.product.main_price * self.product.discount / 100)) * self.quantity

    def coupon_active(self):
        if self.coupon:
            return True
        else:
            return False

    def product_image(self):
        return mark_safe('<img src="{}" heights="70" width="60" />'.format(self.product.image.url))
    product_image.short_description = 'Image'


class Wishlist(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return self.user.first_name+''+self.user.last_name

    def cost(self):
        return (self.product.main_price - (self.product.main_price * self.product.discount / 100)) * self.quantity

    def product_image(self):
        return mark_safe('<img src="{}" heights="70" width="60" />'.format(self.product.image.url))
    product_image.short_description = 'Image'
    
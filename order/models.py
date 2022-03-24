from django.db import models
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe

from django.utils.timezone import now

from product.models import Product, Category
from accounts.models import AddressBook
    


DIS_TYPE = (
    ('Fixed', 'Fixed'),
    ('Percent', 'Percent')
)

class Coupon(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=50)
    discount_type = models.CharField(max_length=20, default="Percent", choices=DIS_TYPE)
    value = models.IntegerField()
    free_shipping = models.BooleanField()
    start_date = models.DateTimeField(default=now)
    end_date = models.DateTimeField()
    min_spend = models.FloatField(blank=True, null=True)
    max_spend = models.FloatField(blank=True, null=True)
    products = models.ManyToManyField(Product, related_name='products')
    exclude_products = models.ManyToManyField(Product, related_name='exclude_products')
    categories = models.ManyToManyField(Category, related_name='categories')
    exclude_categories = models.ManyToManyField(Category, related_name="exclude_categories")
    limit_per_coupon = models.IntegerField(blank=True, null=True)
    limit_per_customer = models.IntegerField(blank=True, null=True)
    active = models.BooleanField(default=True)

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
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_shopcart")
    quantity = models.IntegerField(default=1)
    coupon = models.ForeignKey(Coupon, blank=True, null=True, on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    order_id = models.CharField(max_length=500, blank=True, null=True)
    on_order = models.BooleanField(default=False)

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
        return mark_safe('<img src="{}" heights="70" width="60" />'.format(self.product.image))
    product_image.short_description = 'Image'


class Wishlist(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="pro_wishlist")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="wishlist")
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return self.user.first_name+''+self.user.last_name

    def cost(self):
        return (self.product.main_price - (self.product.main_price * self.product.discount / 100)) * self.quantity

    def product_image(self):
        return mark_safe('<img src="{}" heights="70" width="60" />'.format(self.product.image.url))
    product_image.short_description = 'Image'

    def users_all_wish_pro(self):
        print("I am here ------------------->")
        all_wish = Wishlist.objects.filter(user = self.user)
        lst = []
        for item in all_wish:
            lst.append(item.product.id)
        print(lst)
        return lst

class ShippingMethod(models.Model):
    name = models.CharField(max_length=200)
    fee = models.IntegerField()
    method_type = models.CharField(max_length=100, blank=True, null=True)
    active = models.BooleanField(default=True)
    def __str__(self):
        return self.name

class PaymentMethod(models.Model):
    name = models.CharField(max_length=200)
    client_id = models.TextField()
    secret = models.TextField()
    active = models.BooleanField(default=False)
    def __str__(self):
        return self.name
    

STATUS = (
    ('processing', 'Processing'),
    ('canceled', 'Canceled'),
    ('completed', 'Completed'),
    ('pending', 'Pending'),
    ('pending_payment', 'Pending Payment'),
)

class Order(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE, blank=True, null=True, related_name="user_order")
    shopcarts = models.ManyToManyField(ShopCart)
    payment_id = models.TextField(blank=True, null=True)
    payment_mode = models.CharField(max_length=200, blank=True, null=True)
    company_name = models.CharField(max_length=500, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    region = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    area = models.CharField(max_length=300, blank=True, null=True)
    address = models.CharField(max_length=300, blank=True, null=True)
    shipping_method = models.ForeignKey(ShippingMethod, on_delete=models.DO_NOTHING, blank=True, null=True)
    shipping_fee = models.CharField(max_length=5, blank=True, null=True)
    total = models.FloatField(blank=True, null=True)
    rate = models.FloatField(blank=True, null=True)
    total_bdt = models.FloatField(blank=True, null=True)
    order_date = models.DateTimeField(default=now)
    status = models.CharField(choices=STATUS, max_length=200, default="processing")
    update = models.DateTimeField(default=now)

    def __str__(self):
        return self.user.first_name+" "+self.user.last_name
    
    
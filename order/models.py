from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe
from django.contrib.postgres.fields import ArrayField
from django.utils.timezone import now

from product.models import Product, Category, Option
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

from datetime import date
class Cart(models.Model):
	product = models.ForeignKey(Product, on_delete = models.CASCADE)
	quantity = models.IntegerField(default=1)
	color = models.CharField(max_length=10, blank=True, null=True)
	size = models.CharField(max_length=10, blank=True, null=True)
	options = models.ManyToManyField(Option)

	def total(self):
		main_price = float(self.product.main_price)
		for option in self.options.all():
			main_price += float(option.price)
		main_price -=  (( main_price * float(self.product.discount)) / 100)
		if self.product.hot_deal_end >= date.today():
			if self.product.hot_deal_discount_type == 'percentage':
				main_price -= ((main_price * self.product.hot_deal_discount) / 100)
			else:
				main_price -= self.product.hot_deal_discount
		return main_price

class ShopCart(models.Model):
	carts = models.ManyToManyField(Cart, related_name='parents')
	user = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=True, null=True, related_name="user_shopcart")
	device = models.TextField(blank=True, null=True)
	coupon = models.ManyToManyField(Coupon)
	created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
	order_id = models.CharField(max_length=500, blank=True, null=True)
	on_order = models.BooleanField(default=False)

	def name(self):
		if self.user:
			return self.user.first_name+''+self.user.last_name
		else:
			return self.device

	def coupons(self):
		return self.coupon.all().count()

	def free_ship(self):
		free = False
		for cpn in self.coupon.all():
			if cpn.free_shipping:
				free = True
		return free

class Wishlist(models.Model):
	product = models.ManyToManyField(Product)
	user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
	device = models.TextField(blank=True, null=True)
	created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

	def __str__(self):
		return self.user.first_name+''+self.user.last_name

	def cost(self):
		return (self.product.main_price - (self.product.main_price * self.product.discount / 100)) * self.quantity

	def product_image(self):
		return mark_safe('<img src="{}" heights="70" width="60" />'.format(self.product.image.url))
	product_image.short_description = 'Image'

	def users_all_wish_pro(self):
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
	about = models.TextField(blank=True, null=True)
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
	user = models.ForeignKey(User, on_delete = models.SET_NULL, blank=True, null=True)
	device = models.TextField(blank=True, null=True)
	first_name = models.CharField(max_length=100, blank=True, null=True)
	last_name = models.CharField(max_length=100, blank=True, null=True)
	shopcart = models.ForeignKey(ShopCart, on_delete = models.CASCADE, blank=True, null=True)
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
	ship_name = models.CharField(max_length=50, blank=True, null=True)
	ship_cost = models.CharField(max_length=10, blank=True, null=True)
	coupons = ArrayField(
		ArrayField(
			models.CharField(max_length=100, blank=True, null=True)
		), blank=True, null=True
	)
	coupon_disc = models.CharField(max_length=10, blank=True, null=True)
	total = models.FloatField(blank=True, null=True)
	rate = models.FloatField(blank=True, null=True)
	order_date = models.DateTimeField(default=now)
	status = models.CharField(choices=STATUS, max_length=200, default="processing")
	update = models.DateTimeField(default=now)

	def __str__(self):
		return self.first_name+' '+self.last_name

	def subtotal(self):
		return float(self.total) - float(self.ship_cost) + float(self.coupon_disc)
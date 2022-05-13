from django.db import models
from django.utils.safestring import mark_safe
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from django.template.defaultfilters import slugify
from django.db.models import Q, Sum, Avg
from django.utils.timezone import now
from datetime import date

from datetime import timedelta
from PIL import Image
import json

from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from fontawesome_5.fields import IconField

# from order.models import ShopCart

class Category(models.Model):
	name = models.CharField(max_length=200)
	banner = models.ImageField(upload_to = 'category/banner/', blank=True, null=True)
	icon = models.CharField(max_length=100)
	slug= models.SlugField(null=True, unique=True)
	searchable = models.BooleanField(default=True)
	enable = models.BooleanField(default=True)

	def __str__(self):
		return self.name

	def Total_Group(self):
		return Group.objects.filter(category__id=self.id).count()

	def Total_Subcategory(self):
		return Subcategory.objects.filter(category__id=self.id).count()

	def image_tag(self):
		if self.banner:        
			return mark_safe('<img src="{}" heights="100" width="60" />'.format(self.banner.url))
		else:
			return 'Null'
	image_tag.short_description = 'Banner'


class Group(models.Model):
	name = models.CharField(max_length=200)
	category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='groups')
	slug = models.SlugField(null=True)
	searchable = models.BooleanField(default=True)
	enable = models.BooleanField(default=True)

	def __str__(self):
		return self.name

	def total_subcategory(self):
		return Subcategory.objects.filter(group__id=self.id).count()

class Subcategory(models.Model):
	name = models.CharField(max_length=200)
	category = models.ForeignKey(Category, on_delete=models.CASCADE)
	group = models.ForeignKey(Group, on_delete=models.DO_NOTHING, related_name='subcategorys')
	slug= models.SlugField(null=True)
	searchable = models.BooleanField(default=True)
	enable = models.BooleanField(default=True)

	def __str__(self):
		return self.name

	def total_product(self):
		return Product.objects.filter(category__id=self.id).count()

class Brands(models.Model):
	name = models.CharField(max_length=50)
	logo = models.ImageField(upload_to="product/brand/")

	def __str__(self):
		return self.name

	def image_tag(self):
		return mark_safe('<img src="{}" heights="60" width="60" />'.format(self.logo.url))
	image_tag.short_description = 'Image'


class Option(models.Model):
	label = models.CharField(max_length=100)
	price = models.FloatField(default=0)
	parent_name = models.CharField(max_length=100, blank=True, null=True)

	def __str__(self):
		return self.label

class Options(models.Model):
	name = models.CharField(max_length=100)
	style = models.CharField(max_length=100)
	option = models.ManyToManyField(Option)

	def __str__(self):
		return self.name
	

class Product(models.Model):
	dis_type = (
		('Fixed', 'Fixed'),
		('Percentage', 'Percentage')
	)
	category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='product_categorys', blank=True, null=True)
	group = models.ForeignKey(Group, on_delete=models.DO_NOTHING, blank=True, null=True, related_name = 'product_groups')
	subcategory = models.ForeignKey(Subcategory, on_delete=models.DO_NOTHING, blank=True, null=True, related_name = 'product_subcategorys')
	title = models.CharField(max_length=200)
	image = models.CharField(max_length=500, blank = True, null=True)
	main_price = models.DecimalField(decimal_places=2, max_digits=15)
	discount = models.DecimalField(decimal_places=0, max_digits=3, blank=True, null=True)
	discount_type = models.CharField(max_length=10, choices=dis_type, default="Percentage")
	hot_deal_start = models.DateField(blank=True, null=True)
	hot_deal_end = models.DateField(blank=True, null=True)
	hot_deal_discount = models.IntegerField(blank=True, null=True)
	hot_deal_discount_type = models.CharField(max_length=50, blank=True, null=True)
	hot_deal_free_shipping = models.BooleanField(default=False)
	amount = models.IntegerField(default=3)
	short_info = models.TextField()
	description = RichTextUploadingField()
	additional_info = RichTextUploadingField()
	shipping_info = RichTextUploadingField()
	size = models.CharField(max_length=200, null=True, blank=True)
	color = models.CharField(max_length=500, null=True, blank=True)
	option = models.ManyToManyField(Options, related_name='options', blank=True)
	enable = models.BooleanField(default=True)
	slug = models.SlugField(null=True, unique=True)
	meta_title = models.CharField(max_length=200, null=True, blank=True)
	meta_keywords = models.CharField(max_length=200, null=True, blank=True)
	meta_descriptions = models.CharField(max_length=500, null=True, blank=True)
	related_product = models.CharField(max_length=500, blank=True, null=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	unique = models.TextField(blank=True, null=True)
	total_view = models.IntegerField(default=0)
	rate = models.FloatField(default=0)

	def __str__(self):
		return self.title

	def price(self):
		main_price = float(self.main_price)
		main_price -=  (( main_price * float(self.discount)) / 100)
		if self.hot_deal_end >= date.today():
			if self.hot_deal_discount_type == 'percentage':
				main_price -= ((main_price * self.hot_deal_discount) / 100)
			else:
				main_price -= self.hot_deal_discount
		return main_price

	def pro_color(self):
		clrs = []
		for clr in self.color[2:-2].split("', '"):
			if clr != '':
				clrs.append(clr)
		return clrs

	def pro_size(self):
		return self.size.split(',')
	
	def related_pro(self):
		related_p = []
		if self.related_product != None and len(self.related_product) > 0:
			for id in self.related_product.split(','):
				try:
					pro = Product.objects.get(id = id)
					related_p.append(pro)
				except:
					continue
		return related_p

	def addtional_images(self):
		return Images.objects.filter(unique = self.unique)

	def price_per(self):
		if self.main_price > 0:
			return f"{self.main_price - (self.main_price * self.discount / 100)} (-{self.discount}%)"
		else:
			return 0

	def rating(self):
		rating = Review.objects.filter(product=self).aggregate(Avg('rating'))['rating__avg']
		return rating if type(rating) == float else 0

	def hot_deal_active(self):
		if self.hot_deal_end > date.today():
			return True
		else: return False

	def hd_end(self):
		return self.hot_deal_end+timedelta(1)

	def hd_disc(self):
		if self.hot_deal_discount_type == 'percentage':
			return f'hot deal | {self.hot_deal_discount}% '+' off'
		else: return f'hot deal | {self.hot_deal_discount} off'
    		 

	def total_review(self):
		return Review.objects.filter(product=self).count()

	def image_tag(self):
		return mark_safe('<img src="{}" heights="70" width="60" />'.format(self.image))
	image_tag.short_description = 'Image'

	# def save(self, *args, **kwargs):
	#     if self.image:
	#         super(Product, self).save(*args, **kwargs)
	#         img = Image.open(self.image.path)
	#         if img.height != 600 and img.width != 600:
	#             output_size = (600,600)
	#             img.thumbnail(output_size)
	#             img.save(self.image.path)

class Images(models.Model):
	product = models.ForeignKey(Product, on_delete=models.SET_NULL, related_name="images", null=True, blank=True)
	title = models.CharField(max_length=200, blank=True)
	image = models.TextField(blank=True)
	unique = models.TextField(blank=True, null=True)

	def __str__(self):
		return self.unique

	def pro(self):
		return Product.objects.get(unique=self.unique).title

	def image_tag(self):
		return mark_safe('<img src="{}" heights="70" width="60" />'.format(self.image))
	image_tag.short_description = 'Image'

class RecentlyView(models.Model):
	product = models.ForeignKey(Product, on_delete=models.CASCADE)
	on_create = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.product.title
	
class Review(models.Model):
	product = models.ForeignKey(Product, on_delete = models.CASCADE, related_name="reviews")
	user = models.ForeignKey(User, on_delete = models.CASCADE, blank=True, null=True, related_name="user_review")
	user_name = models.CharField(max_length=200, blank=True, null=True)
	rating = models.IntegerField()
	comment = models.TextField()
	add_on = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.user_name
	
	
	
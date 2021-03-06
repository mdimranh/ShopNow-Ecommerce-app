from django.db import models
from django.utils.safestring import mark_safe

from product.models import Category, Group, Subcategory, Product
from ckeditor_uploader.fields import RichTextUploadingField

import json

from solo.models import SingletonModel
from fontawesome_5.fields import IconField
from django.contrib.postgres.fields import ArrayField

from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.text import slugify
	

BANNER_TYPE = (
	('banner1', 'banner1'),
	('banner2', 'banner2'),
	('banner3', 'banner3'),
	('banner4', 'banner4'),
	('banner5', 'banner5'),
	('banner6', 'banner6'),
	('banner4', 'banner7'),
	('banner8', 'banner8'),
)

class Banner(models.Model):
	title = models.CharField(max_length=100)
	caption1 = models.CharField(max_length=500, blank=True, null=True)
	caption2 = models.CharField(max_length=500, blank=True, null=True)
	caption3 = models.CharField(max_length=500, blank=True, null=True)
	call_to_text = models.CharField(max_length=500, default="Shop Now")
	call_to_url = models.CharField(max_length=500, default="/")
	image = models.ImageField(upload_to = 'banner/')
	banner_type = models.CharField(max_length=50, default='Top', choices=BANNER_TYPE)
	active = models.BooleanField(default=True)

	def ImageUrl(self):
		if self.image:
			return self.image.url
		else:
			return ""
	def image_tag(self):
		return mark_safe('<img src="{}" heights="70" width="60" />'.format(self.image.url))
	image_tag.short_description = 'Image'

	def __str__(self):
		return self.title
	

class Aboutus(models.Model):
	line1 = models.CharField(max_length=250)
	line2 = models.TextField()
	line3 = models.TextField()
	banner = models.ImageField(upload_to='aboutus/banner')

	def ImageUrl(self):
		if self.banner:
			return self.banner.url
		else:
			return ""
	
	def image_tag(self):
		return mark_safe('<img src="{}" heights="70" width="60" />'.format(self.banner.url))
	image_tag.short_description = 'Image'

	def __str__(self):
		return self.line1
	

class TeamInfo(models.Model):
	name = models.CharField(max_length=250)
	job_title = models.CharField(max_length=250)
	email = models.EmailField()
	image = models.ImageField(upload_to = 'aboutus/team/')
	about_us = models.ForeignKey(Aboutus, on_delete = models.CASCADE)

	def __str__(self):
		return self.name
	

	def ImageUrl(self):
		if self.image:
			return self.image.url
		else:
			return ""
	
	def image_tag(self):
		return mark_safe('<img src="{}" heights="70" width="60" />'.format(self.image.url))
	image_tag.short_description = 'Image'

class ContactMessage(models.Model):
	STATUS = (
		('New', 'New'),
		('Read', 'Read'),
		('Closed', 'Closed'),
	)
	name = models.CharField(max_length=200)
	email = models.EmailField()
	subject = models.CharField(max_length=250, blank=True)
	message = models.TextField(blank=True)
	status = models.CharField(max_length=10, choices=STATUS, default='New')
	ip = models.CharField(max_length=100, blank=True)
	note = models.CharField(max_length=200, blank=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self):
			return self.name


class Slider(models.Model):
	name = models.CharField(max_length=250)
	speed = models.IntegerField(default=3000)
	autoplay = models.BooleanField(default=True)
	autoplay_timeout = models.IntegerField(default=4000)
	dots = models.BooleanField(default=True)
	arrows = models.BooleanField(default=True)

	def __str__(self):
		return self.name

	def slides(self):
		return Slide.objects.filter(slider = self).order_by("position")
	
	class Meta:
		verbose_name = 'Slider'

class Slide(models.Model):
	slider = models.ForeignKey(Slider, on_delete = models.CASCADE, related_name="slide")
	caption_1 = models.CharField( max_length=250, verbose_name='caption 1')
	caption_2 = models.CharField( max_length=250, verbose_name='caption 2')
	caption_3 = models.CharField( max_length=250, verbose_name='caption 3')
	action_text = models.CharField( max_length=200, verbose_name='Call to Action Text')
	action_url = models.URLField(verbose_name='Call to Action URL')
	link_type = models.BooleanField(verbose_name='Open in new window')
	image = models.ImageField(upload_to = 'slide/')
	active = models.BooleanField(verbose_name='Status')
	position = models.IntegerField(blank=True, null=True)

	def __str__(self):
		return ''
	

	def ImageUrl(self):
		if self.image:
			return self.image.url
		else:
			return ""

	def image_tag(self):
		return mark_safe('<img src="{}" heights="70" width="60" />'.format(self.image.url))
	image_tag.short_description = 'Image'

# class SiteFront(SingletonModel):
# 	slider = models.ForeignKey(Slider, on_delete = models.DO_NOTHING, blank=True, null=True)
# 	banner1 = models.ForeignKey(Banner, on_delete = models.DO_NOTHING, blank=True, null=True, related_name='banner1')
# 	banner2 = models.ForeignKey(Banner, on_delete = models.DO_NOTHING, blank=True, null=True, related_name='banner2')
# 	banner3 = models.ForeignKey(Banner, on_delete = models.DO_NOTHING, blank=True, null=True, related_name='banner3')
# 	banner4 = models.ForeignKey(Banner, on_delete = models.DO_NOTHING, blank=True, null=True, related_name='banner4')
# 	banner5 = models.ForeignKey(Banner, on_delete = models.DO_NOTHING, blank=True, null=True, related_name='banner5')
# 	banner6 = models.ForeignKey(Banner, on_delete = models.DO_NOTHING, blank=True, null=True, related_name='banner6')
# 	banner7 = models.ForeignKey(Banner, on_delete = models.DO_NOTHING, blank=True, null=True, related_name='banner7')
# 	banner8 = models.ForeignKey(Banner, on_delete = models.DO_NOTHING, blank=True, null=True, related_name='banner8')

# 	def __str__(self):
# 		return "Site Front"

# 	class Meta:
# 		verbose_name = "Site Front"

menu_style = (
	("mega", "Mega Menu"),
	("dropdown", "Dropdown"),
)

class Menus(models.Model):
	name = models.CharField(max_length=100)
	style = models.CharField(max_length=200, choices=menu_style)
	categorys = models.ManyToManyField(Category)
	groups = models.ManyToManyField(Group)
	subcategorys = models.ManyToManyField(Subcategory)
	icon = models.CharField(max_length=200)
	active = models.BooleanField(default=True)
	position = models.IntegerField(blank=True, null=True)

	def __str__(self):
		return self.name

	def cat_group(self):
		group = []
		for cat in self.categorys.all():
			for grp in cat.groups.all():
				group.append(grp)
		return group

	def group_subcat(self):
		subcat = []
		for grp in self.groups.all():
			for sub_cat in grp.subcategorys.all():
				subcat.append(sub_cat)
		return subcat

	def categories_id(self):
		ids = ''
		for item in self.categorys.all():
			if ids == '':
				ids+=str(item.id)
			else:
				ids+=','
				ids+=str(item.id)
		return ids

	def groups_id(self):
		ids = ''
		for item in self.groups.all():
			if ids == '':
				ids+=str(item.id)
			else:
				ids+=','
				ids+=str(item.id)
		return ids

	def subcats_id(self):
		ids = ''
		for item in self.subcategorys.all():
			if ids == '':
				ids+=str(item.id)
			else:
				ids+=','
				ids+=str(item.id)
		return ids	


class Pages(models.Model):
	name = models.CharField(max_length=500)
	body = RichTextUploadingField()
	active = models.BooleanField(default=True)
	slug = models.SlugField(max_length=300, unique=True, blank=True, null=True)

	def __str__(self):
		return self.name


@receiver(pre_save, sender=Pages)
def populate_slug(sender, instance, **kwargs):
	instance.slug = slugify(instance.name)

	
	

class ProductCarousel(models.Model):
	name = models.CharField(max_length=50)
	categories = models.ManyToManyField(Category, blank=True)
	groups = models.ManyToManyField(Group, blank=True)
	subcategorys = models.ManyToManyField(Subcategory, blank=True)
	position = models.IntegerField(blank=True, null=True)
	enable = models.BooleanField(default=True)

	def __str__(self):
		return self.name

	def all_product(self):
		prod = []
		cat_pro = Product.objects.filter(category__in = self.categories.all())
		group_pro = Product.objects.filter(group__in = self.groups.all())
		subcat_pro = Product.objects.filter(subcategory__in = self.subcategorys.all())
		for pro in cat_pro:
			prod.append(pro)
		for pro in group_pro:
			if pro not in prod:
				prod.append(pro)
		for pro in subcat_pro:
			if pro not in prod:
				prod.append(pro)
		return prod

	def no_pro(self):
		prod = []
		cat_pro = Product.objects.filter(category__in = self.categories.all())
		group_pro = Product.objects.filter(group__in = self.groups.all())
		subcat_pro = Product.objects.filter(subcategory__in = self.subcategorys.all())
		for pro in cat_pro:
			prod.append(pro)
		for pro in group_pro:
			if pro not in prod:
				prod.append(pro)
		for pro in subcat_pro:
			if pro not in prod:
				prod.append(pro)
		return len(prod)

	def categories_id(self):
		ids = ''
		for item in self.categories.all():
			if ids == '':
				ids+=str(item.id)
			else:
				ids+=','
				ids+=str(item.id)
		return ids

	def groups_id(self):
		ids = ''
		for item in self.groups.all():
			if ids == '':
				ids+=str(item.id)
			else:
				ids+=','
				ids+=str(item.id)
		return ids

	def subcats_id(self):
		ids = ''
		for item in self.subcategorys.all():
			if ids == '':
				ids+=str(item.id)
			else:
				ids+=','
				ids+=str(item.id)
		return ids

class SiteConfiguration(SingletonModel):
	name = models.CharField(max_length=255, default='Buy Now')
	privacy_policy = models.ForeignKey(Pages, on_delete=models.DO_NOTHING, related_name='privacy_policy', blank=True, null=True)
	term_condition = models.ForeignKey(Pages, on_delete=models.DO_NOTHING, related_name='term_condition', blank=True, null=True)
	phone = models.CharField(max_length=20, default = 1, blank=True, null=True)
	logo = models.ImageField(upload_to='settings/', default = 'settings/logo.png')
	address=models.CharField(max_length=200, default = 'Dhaka')
	email = models.EmailField(blank=True, null=True)
	twitter = models.URLField(default = 'twitter.com')
	facebook = models.URLField(default = 'facebook.com')
	youtube = models.URLField(default = 'youtube.com')
	instagram = models.URLField(default = 'instagram.com')
	favicon = models.ImageField(upload_to='settings/')
	slider = models.ForeignKey(Slider, on_delete = models.DO_NOTHING, blank=True, null=True)
	banner1 = models.ForeignKey(Banner, on_delete = models.DO_NOTHING, blank=True, null=True, related_name='banner1')
	banner2 = models.ForeignKey(Banner, on_delete = models.DO_NOTHING, blank=True, null=True, related_name='banner2')
	banner3 = models.ForeignKey(Banner, on_delete = models.DO_NOTHING, blank=True, null=True, related_name='banner3')
	banner4 = models.ForeignKey(Banner, on_delete = models.DO_NOTHING, blank=True, null=True, related_name='banner4')
	banner5 = models.ForeignKey(Banner, on_delete = models.DO_NOTHING, blank=True, null=True, related_name='banner5')
	banner6 = models.ForeignKey(Banner, on_delete = models.DO_NOTHING, blank=True, null=True, related_name='banner6')
	banner7 = models.ForeignKey(Banner, on_delete = models.DO_NOTHING, blank=True, null=True, related_name='banner7')
	banner8 = models.ForeignKey(Banner, on_delete = models.DO_NOTHING, blank=True, null=True, related_name='banner8')
	maintenance_mode = models.BooleanField(default=False)

	def __str__(self):
		return "Site Configuration"

	class Meta:
		verbose_name = "Site Configuration"

class Feature(SingletonModel):
	title1 = models.CharField(max_length=300, blank=True, null=True)
	subtitle1 = models.CharField(max_length=300, blank=True, null=True)
	icon1 = models.CharField(max_length=100, blank=True, null=True)
	title2 = models.CharField(max_length=300, blank=True, null=True)
	subtitle2 = models.CharField(max_length=300, blank=True, null=True)
	icon2 = models.CharField(max_length=100, blank=True, null=True)
	title3 = models.CharField(max_length=300, blank=True, null=True)
	subtitle3 = models.CharField(max_length=300, blank=True, null=True)
	icon3 = models.CharField(max_length=100, blank=True, null=True)
	title4 = models.CharField(max_length=300, blank=True, null=True)
	subtitle4 = models.CharField(max_length=300, blank=True, null=True)
	icon4 = models.CharField(max_length=100, blank=True, null=True)

class Links(models.Model):
	name = models.CharField(max_length=50, blank=True, null=True)
	link = models.URLField()

class FooterLinks(models.Model):
	section_name = models.CharField(max_length=200)
	links = models.ManyToManyField(Links)

class Currency(models.Model):
	symbol = models.CharField(max_length=10)
	name = models.CharField(max_length=100)
	symbol_native = models.CharField(max_length=5)
	rate = models.FloatField(default=1)
	decimal_digits = models.CharField(max_length=2)
	code = models.CharField(max_length=10)
	name_plural = models.CharField(max_length=100)
	active = models.BooleanField(default=True)

	def __str__(self):
		return self.name
			


class Settings(models.Model):
	default_currency = models.ForeignKey(Currency, on_delete=models.CASCADE, related_name='defailt_currency')
	supported_currency = models.ManyToManyField(Currency, related_name='supported_currency')
	welcome_email = models.BooleanField(default=True)
	order_email = models.BooleanField(default=True)
	order_status_email = models.BooleanField(default=True)
	invoice_email = models.BooleanField(default=True)

class EmailConfig(SingletonModel):
	email_host = models.CharField(max_length=200)
	email_port = models.CharField(max_length=20)
	email_use = models.CharField(max_length=10)
	email_host_user = models.CharField(max_length=100)
	email_host_password = models.CharField(max_length=50)

class StoreInfo(SingletonModel):
	tagline = models.TextField()
	phone = models.CharField(max_length=20)
	email = models.EmailField()
	address1 = models.TextField()
	address2 = models.TextField()
	city = models.CharField(max_length=100)
	country = models.CharField(max_length=50)
	state = models.CharField(max_length=100)
	zip = models.CharField(max_length=50)
	
	
	
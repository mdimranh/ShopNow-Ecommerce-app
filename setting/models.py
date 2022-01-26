from django.db import models
from django.utils.safestring import mark_safe

from product.models import Category, Group, Subcategory

import json

from solo.models import SingletonModel
from fontawesome_5.fields import IconField

class SiteConfiguration(SingletonModel):
	name = models.CharField(max_length=255, default='Buy Now')
	phone = models.CharField(max_length=20, default = 1)
	logo = models.ImageField(upload_to='settings/', default = 'settings/logo.png')
	address=models.CharField(max_length=200, default = 'Dhaka')
	twitter = models.URLField(default = 'twitter.com')
	facebook = models.URLField(default = 'facebook.com')
	youtube = models.URLField(default = 'youtube.com')
	instagram = models.URLField(default = 'instagram.com')
	favicon = models.ImageField(upload_to='settings/')
	maintenance_mode = models.BooleanField(default=False)

	def __str__(self):
		return "Site Configuration"

	class Meta:
		verbose_name = "Site Configuration"
	

BANNER_TYPE = (
	('Left', 'Left'),
	('Top', 'Top'),
	('Middle Small', 'Middle Small'),
	('Middle Big', 'Middle Big'),
	('Bottom', 'Bottom')
)

class Banner(models.Model):
	title = models.CharField(max_length=100)
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
	autoplay = models.BooleanField(default=True)
	autoplay_timeout = models.IntegerField(default=4000)
	arrows = models.BooleanField(default=True)

	def __str__(self):
		return self.name
	
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

class SiteFront(SingletonModel):
	slider = models.ForeignKey(Slider, on_delete = models.DO_NOTHING, blank=True, null=True)
	top_banner = models.ForeignKey(Banner, on_delete = models.DO_NOTHING, blank=True, null=True, related_name='top_banner')
	left_banner1 = models.ForeignKey(Banner, on_delete = models.DO_NOTHING, blank=True, null=True, related_name='left_banner1')
	left_banner2 = models.ForeignKey(Banner, on_delete = models.DO_NOTHING, blank=True, null=True, related_name='left_banner2')
	middle_big_banner1 = models.ForeignKey(Banner, on_delete = models.DO_NOTHING, blank=True, null=True, related_name='middle_big_banner1')
	middle_big_banner2 = models.ForeignKey(Banner, on_delete = models.DO_NOTHING, blank=True, null=True, related_name='middle_big_banner2')
	middle_small_banner = models.ForeignKey(Banner, on_delete = models.DO_NOTHING, blank=True, null=True, related_name='middle_small_banner')
	bottom_banner1 = models.ForeignKey(Banner, on_delete = models.DO_NOTHING, blank=True, null=True, related_name='bottom_banner1')
	bottom_banner2 = models.ForeignKey(Banner, on_delete = models.DO_NOTHING, blank=True, null=True, related_name='bottom_banner2')

	def __str__(self):
		return "Site Front"

	class Meta:
		verbose_name = "Site Front"

menu_style = (
	("mega", "Mega Menu"),
	("dropdown", "Dropdown"),
)

class Menus(models.Model):
	name = models.CharField(max_length=100)
	style = models.CharField(max_length=200, choices=menu_style)
	categorys = models.ManyToManyField(Category, blank=True)
	groups = models.ManyToManyField(Group, blank=True)
	icon = IconField()

	def __str__(self):
		return self.name
	

class ProductCarousel(models.Model):
	name = models.CharField(max_length=50)
	categories = models.ManyToManyField(Category, blank=True)
	groups = models.ManyToManyField(Group, blank=True)
	subcategorys = models.ManyToManyField(Subcategory, blank=True)
	enable = models.BooleanField(default=True)

	def __str__(self):
		return self.name
	
	
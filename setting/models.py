from django.db import models
from django.utils.safestring import mark_safe

class Banner(models.Model):
	title = models.CharField(max_length=100)
	image = models.ImageField(upload_to = 'banner/')
	big_banner = models.BooleanField(default=False)
	active = models.BooleanField(default=True)

	def ImageUrl(self):
		if self.image:
			return self.image.url
		else:
			return ""
	def image_tag(self):
		return mark_safe('<img src="{}" heights="70" width="60" />'.format(self.image.url))
	image_tag.short_description = 'Image'

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

class TeamInfo(models.Model):
	name = models.CharField(max_length=250)
	job_title = models.CharField(max_length=250)
	email = models.EmailField()
	image = models.ImageField(upload_to = 'aboutus/team/')
	about_us = models.ForeignKey(Aboutus, on_delete = models.CASCADE)

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

class ShopInfo(models.Model):
	name = models.CharField(max_length=50)
	phone=models.CharField(max_length=17)
	email=models.EmailField()
	address=models.CharField(max_length=200)
	twitter = models.URLField()
	facebook = models.URLField()
	youtube = models.URLField()
	instagram = models.URLField()
	logo = models.ImageField(upload_to='shopinfo')
	favicon = models.ImageField(upload_to='shopinfo')

	def __str__(self):
		return self.name


class Sliding(models.Model):
	line_1 = models.TextField(verbose_name='Line 1')
	line_2 = models.TextField(verbose_name='Line 2')
	line_3 = models.TextField(verbose_name='Line 3')
	image = models.ImageField(upload_to = 'slide/')
	active = models.BooleanField(verbose_name='Status')

	def ImageUrl(self):
		if self.image:
			return self.image.url
		else:
			return ""

	def image_tag(self):
		return mark_safe('<img src="{}" heights="70" width="60" />'.format(self.image.url))
	image_tag.short_description = 'Image'
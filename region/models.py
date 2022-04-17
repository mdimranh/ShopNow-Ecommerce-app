from django.db import models

class Country(models.Model):
	name = models.CharField(max_length=100)
	enable = models.BooleanField(default=True)

	def __str__(self):
		return self.name

class Region(models.Model):
	country = models.ForeignKey(Country, on_delete=models.CASCADE, blank=True, null=True, related_name = "region")
	name = models.CharField(max_length=100)
	enable = models.BooleanField(default=True)

	def __str__(self):
		return self.name

class City(models.Model):
	region = models.ForeignKey(Region, on_delete=models.CASCADE, blank=True, null=True, related_name = "city")
	name = models.CharField(max_length=100)
	enable = models.BooleanField(default=True)

	def __str__(self):
		return self.name

class Area(models.Model):
	city = models.ForeignKey(City, on_delete=models.CASCADE, blank=True, null=True, related_name = "area")
	name = models.CharField(max_length=100)
	enable = models.BooleanField(default=True)

	def __str__(self):
		return self.name
	
	
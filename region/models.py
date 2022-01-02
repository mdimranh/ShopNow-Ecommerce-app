from django.db import models

region_choice = [
	('1', 'Asia'),
	('2', 'America')
]

country_choice = [
	('1', 'Bangladesh'),
	('2', 'India')
]

state_choice = [
	('1', 'Dhaka'),
	('2', 'Gazipur')
]

city_choice = [
	('1', 'Mirpur'),
	('2', 'Dhanmondi')
]

class Regions(models.Model):
	name = models.CharField(max_length=50, unique=True)
	region = models.CharField(max_length=50, choices=region_choice, unique=True)

	def __str__(self):
		return self.name

	class Meta:
		verbose_name_plural = 'Regions'
	

class Country(models.Model):
	region = models.ForeignKey(Regions, on_delete = models.CASCADE)
	name = models.CharField(max_length=50, unique=True)
	country = models.CharField(max_length=100, choices=country_choice)

	def __str__(self):
		return self.name


class State(models.Model):   #district
	country = models.ForeignKey(Country, on_delete=models.CASCADE)
	name = models.CharField(max_length=100)
	state = models.CharField(max_length=100, choices=state_choice)

	def __str__(self):
		return self.name

class City(models.Model):
	state = models.ForeignKey(State, on_delete=models.CASCADE)
	name = models.CharField(max_length=100)
	city = models.CharField(max_length=100, choices=city_choice)

	def __str__(self):
		return self.name

class Area(models.Model):
	name = models.CharField(max_length=50, unique=True)
	city = models.ForeignKey(City, on_delete = models.CASCADE)

	def __str__(self):
		return self.name



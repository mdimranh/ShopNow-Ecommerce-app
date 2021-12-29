from django.shortcuts import render

from .models import SiteConfiguration
config = SiteConfiguration.objects.get()
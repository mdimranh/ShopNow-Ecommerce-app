from django.shortcuts import render

from .models import SiteConfiguration
config = SiteConfiguration.objects.get()

from .models import SiteFront
config = SiteFront.objects.get()
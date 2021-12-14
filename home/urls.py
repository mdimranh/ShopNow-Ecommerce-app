from django.urls import path
from .views import *

urlpatterns = [
    path('', Home, name='home'),
    path('about-us', AboutUs, name='aboutus'),
    path('contact', ContactUs, name='contactus'),
    path('search', SearchView, name='search'),
]

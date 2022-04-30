from django.urls import path
from .views import *

urlpatterns = [
    path('', Home, name="home"),
    path('search', SearchView, name='search'),
    path('page/<slug:slug>', PageView.as_view(), name='page'),
]

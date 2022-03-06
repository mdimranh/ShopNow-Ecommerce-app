from django.urls import path
from .views import Account, Logout, ProfileView, GetCity, GetRegion, GetArea

urlpatterns = [
    path('auth/', Account, name = 'login'),
    path('profile', ProfileView, name = 'profile'),
    path('auth/logout', Logout, name = 'logout'),
    path('get-city', GetCity, name = 'getcity'),
    path('get-region', GetRegion, name = 'getregion'),
    path('get-area', GetArea, name = 'getarea')
]

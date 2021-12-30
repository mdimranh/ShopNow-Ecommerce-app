from django.urls import path
from .views import Account, Logout, Profile, GetCity, GetArea

urlpatterns = [
    path('auth/', Account, name = 'login'),
    path('profile', Profile, name = 'profile'),
    path('auth/logout', Logout, name = 'logout'),
    path('city/', GetCity, name = 'getcity'),
    path('area/', GetArea, name = 'getarea')
]

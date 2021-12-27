from django.urls import path
from .views import Account, Logout, Profile

urlpatterns = [
    path('auth/', Account, name = 'login'),
    path('profile', Profile, name = 'profile'),
    path('auth/logout', Logout, name = 'logout')
]

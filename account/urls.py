from django.urls import path
from .views import Account, Logout

urlpatterns = [
    path('auth/', Account, name = 'login'),
    path('auth/logout', Logout, name = 'logout')
]

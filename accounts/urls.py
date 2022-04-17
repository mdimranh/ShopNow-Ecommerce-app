from django.urls import path
from .views import Account, Logout, ProfileView, GetCity, GetRegion, GetArea, DeleteUser, DeleteGroup , emailConfirm, passwordRecover

urlpatterns = [
    path('auth/', Account, name = 'login'),
    path('verify/<str:activation_key>', emailConfirm, name='email_confirm'),
    path('password_recover/<str:activation_key>', passwordRecover, name='password_recover'),
    path('profile', ProfileView, name = 'profile'),
    path('auth/logout', Logout, name = 'logout'),
    path('get-city', GetCity, name = 'getcity'),
    path('get-region', GetRegion, name = 'getregion'),
    path('get-area', GetArea, name = 'getarea'),
    path('user/delete-user', DeleteUser.as_view(), name='dleteuser'),
    path('group/delete-group', DeleteGroup.as_view(), name='dletegroup')
]

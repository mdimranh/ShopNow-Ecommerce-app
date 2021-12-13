from django.urls import path
from .views import ProductDetails

urlpatterns = [
    path('products/<int:id>', ProductDetails, name='productdetails')
]

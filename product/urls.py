from django.urls import path
from .views import ProductDetails, CategoryProduct, CategoryGroupList, ProductGroupList, ControlCayegoryList

urlpatterns = [
    path('products/<int:id>', ProductDetails, name='productdetails'),
    path('category/<int:id>/<slug:slug>', CategoryProduct, name='category_product'),
    path('groups/', CategoryGroupList.as_view()),
    path('productgroups/', ProductGroupList.as_view()),
    path('control/productgroups/', ControlCayegoryList.as_view()),
]

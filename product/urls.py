from django.urls import path
from .views import ProductDetails, CategoryProduct, CategoryGroupList, ProductGroupList, ControlCategoryList

urlpatterns = [
    path('products/<int:id>', ProductDetails, name='productdetails'),
    path('products/<str:type>/<int:id>', CategoryProduct.as_view()),
    path('groups/', CategoryGroupList.as_view()),
    path('productgroups', ProductGroupList.as_view()),
    path('control/productgroups', ControlCategoryList.as_view()),
]

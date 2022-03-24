from rest_framework import serializers
from product.models import Product, Category
from order.models import ShopCart, Wishlist

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from django.contrib.auth.models import User
from accounts.models import Profile, AddressBook

from django.conf import settings

class ProductListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'image', 'main_price', 'price', 'discount', 'discount_type', 'rating', 'total_review', 'hot_deal_end']

class ProductDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        # fields = ['id', 'title', 'image', 'main_price', 'price', 'discount', 'discount_type', 'rating', 'total_review', 'hot_deal_end']
        fields = '__all__'

class CategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'searchable', 'enable']

class CategoryDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'searchable', 'enable']

class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # fields = '__all__'
        exclude = ['username']

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)
        data['type'] = settings.SIMPLE_JWT['AUTH_HEADER_TYPES'][0]
        data['lifetime'] = str(settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'].days)+'days'
        return data

class ShopcartSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShopCart
        fields = '__all__'

class WishlistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wishlist
        fields = '__all__'

class ShopcartSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShopCart
        fields = '__all__'

class UserSrializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email']

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        exclude = ['online', 'image', 'user']

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = AddressBook
        exclude = ['temp', 'user']
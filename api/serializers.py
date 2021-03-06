from rest_framework import serializers
from product.models import *
from order.models import ShopCart, Cart, Wishlist
from setting.models import ProductCarousel

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from django.contrib.auth.models import User
from accounts.models import Profile, AddressBook
from region.models import *

from django.conf import settings

class ReviewSerializer(serializers.ModelSerializer):
	user = serializers.CurrentUserDefault()
	class Meta:
		model = Review
		fields = '__all__'

class CategoryDetailsSerializer(serializers.ModelSerializer):
	class Meta:
		model = Category
		fields = ['id', 'name', 'slug', 'searchable', 'enable']

class GroupDetailsSerializer(serializers.ModelSerializer):
	class Meta:
		model = Group
		fields = ['id', 'name', 'slug', 'searchable', 'enable']

class SubcategoryDetailsSerializer(serializers.ModelSerializer):
	class Meta:
		model = Subcategory
		fields = ['id', 'name', 'slug', 'searchable', 'enable']

class ProductListSerializer(serializers.ModelSerializer):
	category = CategoryDetailsSerializer()
	class Meta:
		model = Product
		fields = ['id', 'title', 'image', 'main_price', 'price', 'discount', 'discount_type', 'category', 'rating', 'total_review', 'hot_deal_discount', 'hot_deal_discount_type', 'hot_deal_end', 'price']

class ProductDetailsSerializer(serializers.ModelSerializer):
	category = CategoryDetailsSerializer()
	group = GroupDetailsSerializer()
	subcategory = SubcategoryDetailsSerializer()
	review = serializers.SerializerMethodField()
	rating = serializers.SerializerMethodField()
	price = serializers.SerializerMethodField()

	class Meta:
		model = Product
		exclude = ['slug', 'meta_title', 'meta_keywords', 'meta_descriptions', 'unique', 'rate']

	def get_review(self, obj):
		rv = Review.objects.filter(product__id = obj.id)
		rvw = ReviewSerializer(rv, many=True)
		return rvw.data

	def get_rating(self, obj):
		rating = Review.objects.filter(product__id = obj.id).aggregate(Avg('rating'))['rating__avg']
		return rating

	def get_price(self, obj):
		main_price = float(obj.main_price)
		main_price -=  (( main_price * float(obj.discount)) / 100)
		if obj.hot_deal_end >= date.today():
			if obj.hot_deal_discount_type == 'percentage':
				main_price -= ((main_price * obj.hot_deal_discount) / 100)
			else:
				main_price -= obj.hot_deal_discount
		return main_price


class CategoryListSerializer(serializers.ModelSerializer):
	class Meta:
		model = Category
		fields = ['id', 'name', 'slug', 'searchable', 'enable']

class RegistrationSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = '__all__'

	def validate(self, obj):
		errors = {}
		required_fields = ['email', 'first_name', 'last_name', 'password']
		for field in required_fields:
			if field not in obj:
				errors[field] = 'This field is required.'
			
			if errors:
				raise serializers.ValidationError(errors)
		return obj

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
	carts = serializers.SerializerMethodField()
	class Meta:
		model = ShopCart
		exclude = ['device', 'created_at', 'order_id', 'on_order', 'user']

	def get_carts(self, obj):
		cart_list = obj.carts.all()
		serializer = CartSerializer(cart_list, many=True)
		return serializer.data

class CartSerializer(serializers.ModelSerializer):
	product = serializers.SerializerMethodField()
	class Meta:
		model = Cart
		fields = '__all__'

	def get_product(self, obj):
		pro = ProductDetailsSerializer(obj.product, many=False)
		data = {
			'title': pro.data['title'],
			'img': pro.data['image'],
			'category':{
				'id': pro.data['category']['id'],
				'name': pro.data['category']['name']
			},
			'main_price': float(pro.data['main_price']),
			'price': pro.data['price'],
			'rating': pro.data['rating']
		}
		return data

class WishlistSerializer(serializers.ModelSerializer):
	class Meta:
		model = Wishlist
		fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		exclude = ['password']

class ProfileSerializer(serializers.ModelSerializer):
	class Meta:
		model = Profile
		exclude = ['online', 'image', 'user']

class AddressSerializer(serializers.ModelSerializer):
	class Meta:
		model = AddressBook
		exclude = ['temp', 'user']

class RegionSerializer(serializers.ModelSerializer):
	class Meta:
		model = Region
		fields = '__all__'

class CitySerializer(serializers.ModelSerializer):
	class Meta:
		model = City
		fields = '__all__'

class AreaSerializer(serializers.ModelSerializer):
	class Meta:
		model = Area
		fields = '__all__'


class ProductCarouselSerializer(serializers.ModelSerializer):
	products = serializers.SerializerMethodField()

	class Meta:
		model = ProductCarousel
		exclude = ['enable', 'categories', 'groups', 'subcategorys']

	def get_products(self, obj):
		prod = []
		cat_pro = Product.objects.filter(category__in = obj.categories.all())
		group_pro = Product.objects.filter(group__in = obj.groups.all())
		subcat_pro = Product.objects.filter(subcategory__in = obj.subcategorys.all())
		for pro in cat_pro:
			prod.append(pro)
		for pro in group_pro:
			if pro not in prod:
				prod.append(pro)
		for pro in subcat_pro:
			if pro not in prod:
				prod.append(pro)
		
		return ProductListSerializer(prod, many=True).data
from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.models import User

from product.models import Product, Category
from order.models import ShopCart, Order
from accounts.models import AddressBook
from region.models import *

from .serializers import *

from django.dispatch import receiver
from django.db.models.signals import pre_save

from datetime import date, timedelta

from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, RetrieveUpdateAPIView, ListCreateAPIView
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView

class Products(ListAPIView):
	serializer_class = ProductListSerializer
	queryset = Product.objects.all()

class ProductDetails(RetrieveAPIView):
	lookup_field = 'id'
	queryset = Product.objects.all()
	serializer_class = ProductDetailsSerializer

class Categories(ListAPIView):
	serializer_class = CategoryListSerializer
	queryset = Category.objects.all()

class CategoryDetails(RetrieveAPIView):
	lookup_field = 'id'
	queryset = Category.objects.all()
	serializer_class = CategoryDetailsSerializer

@permission_classes([IsAuthenticated,])
class AddReview(APIView):
	def post(self, request, format=None):
		errors = {}
		if 'product_id' not in request.POST:
			errors['product_id'] = 'product_id is required.'
		if 'comment' not in request.POST:
			errors['comment'] = 'comment is required.'
		if 'rating' not in request.POST:
			errors['rating'] = 'rating is required.'
		if len(errors) > 0:
			return Response(errors)
		else:
			review = Review(
				user = request.user,
				rating = request.data['rating'],
				product = Product.objects.get(id = request.data['product_id']),
				comment = request.data['comment']
			)
			review.save()
			serializers = ReviewSerializer(review, many=False)
			return Response(serializers.data)

@receiver(pre_save, sender=Review)
def review_user_name(sender, instance, *args, **kwargs):
	if instance.user:
		user = instance.user
		instance.user_name = user.first_name+' '+user.last_name


@api_view(['POST'])
def RegistrationApi(request):
	if request.method == 'POST':
		data = {}
		def error(var):
			data[f'{var}'] = f'{var} is required'
			return Response(data)
		if 'first_name' not in request.POST:
			error('first_name')
		elif 'last_name' not in request.POST:
			error('last_name')
		elif 'email' not in request.POST:
			error('email')
		elif 'password' not in request.POST:
			error('password')
		else:
			serializer = RegistrationSerializer(data=request.data)
			if serializer.is_valid():
				user = serializer.save()
				user.username = request.data['email']
				user.save()
				data['response'] = 'Successfully registration'
				data['username'] = user.username
				data['email'] = user.email
				data['first_name'] = user.first_name
				data['last_name'] = user.last_name
			else:
				data['response'] = serializer.errors
	return Response(data)

class tokenApi(TokenObtainPairView):
	serializer_class = MyTokenObtainPairSerializer

@permission_classes([IsAuthenticated,])
class UserDetails(RetrieveUpdateAPIView):
	queryset = User.objects.all()
	serializer_class = UserSerializer
	lookup_field = 'id'


@api_view(['GET'])
@permission_classes([IsAuthenticated,])
def MyShopcart(request):
	scart, create = ShopCart.objects.get_or_create(user = request.user)
	serializers = ShopcartSerializer(scart, many=False)
	return Response(serializers.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated,])
def MyWishlist(request):
	wlist = Wishlist.objects.filter(user = request.user)
	serializers = WishlistSerializer(wlist, many=True)
	return Response(serializers.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated,])
def DeleteWishlist(request, id):
	wlist = Wishlist.objects.get(id = id)
	wlist.delete()
	wlist = Wishlist.objects.filter(user = request.user)
	serializers = WishlistSerializer(wlist, many=True)
	return Response(serializers.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated,])
def AddddToCart(request):
	errors = {}
	for var in ['product_id', 'quantity']:
		if var not in request.POST:
			errors[f'{var}'] = 'This field is required'
	if len(errors) > 0:
		return Response(errors)
	else:
		scart, create = ShopCart.objects.get_or_create(user = request.user)
		pro_id = int(request.POST['product_id'])
		if Product.objects.filter(id = pro_id).exists():
			pro_list = list(scart.carts.values_list('product__id', flat=True))
			if pro_id in pro_list:
				return JsonResponse({'message': "Product already exist to your cart."})
			pro = Product.objects.get(id = pro_id)
			if pro.amount < 0:
				return JsonResponse({'message': "Out of stock"})
			else:
				try:
					color = request.data['color']
				except:
					color = None
				try:
					size = request.data['size']
				except:
					size = None
				cart = Cart(
					product= pro,
					quantity = request.data['quantity'],
					color=color,
					size=size
				)
				cart.save()
				scart.carts.add(cart)
				try:
					for opt_id in request.data['options'][1:-1].replace(' ', '').split(','):
						option = Option.objects.get(id = opt_id)
						cart.options.add(option)
				except:
					pass
				try:
					Wishlist.objects.filter(product = pro, user = request.user).first().delete()
				except:
					pass
				serializers = ShopcartSerializer(scart, many=False)
				return Response(serializers.data)
		else:
			return Response({'message': "Product is not exist."})
	

@permission_classes([IsAuthenticated,])
class AddressBookDetails(APIView):
	def get(self, request, id, format=None):
		address = AddressBook.objects.get(id = id)
		address_serializers = AddressSerializer(address, many=False)
		regions = RegionSerializer(Region.objects.filter(country=address.country), many=True)
		cities = CitySerializer(City.objects.filter(region=address.region), many=True)
		areas = AreaSerializer(Area.objects.filter(city=address.city), many=True)
		context = {
			'address' : address_serializers.data,
			'regions': regions.data,
			'cities': cities.data,
			'areas': areas.data,
		}
		return Response(context)

	# def post(self, request, format=None):
	#     if Profile.objects.get(user = request.user):
	#         pro = Profile.objects.get(user = request.user)
	#         pro.phone = request.data['phone']
	#         pro.address = request.data['address']
	#         pro.city = request.data['city']
	#         pro.country = request.data['country']
	#         pro.save()
	#         pro_ser = ProfileSerializer(pro, many=False)
	#         return Response(pro_ser.data)
	#     pro = Profile.objects.create(
	#         user = request.user,
	#         phone = request.data['phone'],
	#         address = request.data['address'],
	#         city = request.data['city'],
	#         country = request.data['country']
	#     )
	#     pro_ser = ProfileSerializer(pro, many=False)
	#     return Response(pro_ser.data)

from order.cartdetails import cartDetails
@permission_classes([IsAuthenticated,])
class TotalCartCost(APIView):
	def get(self, request, id, format=None):
		scart = ShopCart.objects.get(id = id)
		cart = cartDetails(scart)
		context = {
			'total' : cart.subtotal + cart.ship_cost - cart.coupon_discount,
		}
		return Response(context)

@permission_classes([AllowAny,])
class Registration(CreateAPIView):
	queryset = User.objects.all()
	serializer_class = RegistrationSerializer

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated,])
def complexProducts(request, data_type):

	if data_type == 'new-product':
		if 'date_range' not in request.POST:
			error = {'date_range': 'This field is required.'}
			return Response(error)
		else:
			from_date = date.today()-timedelta(int(request.data['date_range']))
			queryset = Product.objects.filter(enable=True, created_at__gte=from_date).order_by('-id')
			serializer = ProductListSerializer(queryset, many=True)
			return Response(serializer.data)

	if data_type == 'hot-product':
		queryset = Product.objects.filter(enable=True, hot_deal_end__gte = date.today()).order_by('-id')
		serializer = ProductListSerializer(queryset, many=True)
		return Response(serializer.data)

	if data_type == 'recently-viewed':
		if 'no_of_product' not in request.POST:
			error = {'no_of_product': 'This field is required.'}
			return Response(error)
		else:
			try:
				no_of_product = int(request.data['no_of_product'])
			except:
				error = {'no_of_product': 'Value must be integer.'}
				return Response(error)
			queryset = list(RecentlyView.objects.all().order_by('-on_create').values_list('product', flat=True))
			products = Product.objects.filter(id__in = queryset)[:no_of_product]
			serializer = ProductListSerializer(products, many=True)
			return Response(serializer.data)

	if data_type == 'best-sold':
		if 'date_range' not in request.POST:
			error = {'date_range': 'This field is required.'}
			return Response(error)
		else:
			try:
				bestSell_range = date.today() - timedelta(days = int(request.data['date_range']))
				best_sell = Order.objects.filter(order_date__gte = bestSell_range)
				bs_pro_list = []
				for order in best_sell:
					for cart in order.shopcart.carts.all():
						bs_pro_list.append(cart.product.id)
				bs_pro_list = sorted(bs_pro_list, key=lambda x:[bs_pro_list.count(x), x])
				bs_pro_list.reverse()
				bs_pro_list = list(dict.fromkeys(bs_pro_list))
				bs_pro = []
				for pro_id in bs_pro_list[:5]:
					bs_pro.append(Product.objects.get(id = pro_id))
				serializer = ProductListSerializer(bs_pro, many=True)
				return Response(serializer.data)
			except:
				error = {'date_range': 'Value must be integer.'}
				return Response(error)

	if data_type == 'latest-sold':
		if 'no_of_product' not in request.POST:
			error = {'no_of_product': 'This field is required.'}
			return Response(error)
		else:
			try:
				latest_sold = Order.objects.all().order_by('order_date')
				for order in latest_sold:
					for cart in order.shopcart.carts.all():
						if cart.product not in ls:
							ls.append(cart.product)
							if len(ls) > int(request.data['no_of_product']):
								break
					if len(ls) > int(request.data['no_of_product']):
						break
				serializer = ProductListSerializer(ls, many=True)
				return Response(serializer.data)
			except:
				error = {'no_of_product': 'Value must be integer.'}
				return Response(error)

	if data_type == 'product-carousel':
		product_carousel = ProductCarousel.objects.filter(enable = True)
		serializer = ProductCarouselSerializer(product_carousel, many=True)
		return Response(serializer.data)

	else:
		context = {
			'error': 'Page not found'
		}
		return Response(context)
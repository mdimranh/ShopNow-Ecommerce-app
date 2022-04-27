from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.models import User

from product.models import Product, Category
from order.models import ShopCart
from accounts.models import AddressBook
from region.models import *

from .serializers import *

from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView

def Products(request):
    pro = Product.objects.all()
    serializer = ProductListSerializer(pro, many=True)
    return JsonResponse(serializer.data, safe=False)

def ProductDetail(request, id):
    pro = Product.objects.get(id = id)
    serializer = ProductDetailsSerializer(pro, many=False)
    return JsonResponse(serializer.data, safe=False)

def Categories(request):
    cats = Category.objects.all()
    serializer = CategoryListSerializer(cats, many=True)
    return JsonResponse(serializer.data, safe=False)

def CategoryDetails(request, id):
    cat = Category.objects.get(id = id)
    serializer = CategoryDetailsSerializer(cat, many=False)
    return JsonResponse(serializer.data, safe=False)

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
class UserDetails(APIView):
    def get(self, request, format=None):
        usr = User.objects.get(id = request.user.id)
        serializers = UserSrializer(usr, many=False)
        pro, create = Profile.objects.get_or_create(user = request.user)
        pro_ser = ProfileSerializer(pro, many=False)
        add_book = AddressBook.objects.filter(user = request.user)
        add_ser = AddressSerializer(add_book, many=True)
        lst = {'user' : serializers.data,
            'profile' : pro_ser.data,
            'address' : add_ser.data
        }
        return Response(lst)
    def post(self, request, format=None):
        if Profile.objects.get(user = request.user):
            pro = Profile.objects.get(user = request.user)
            pro.phone = request.data['phone']
            pro.address = request.data['address']
            pro.city = request.data['city']
            pro.country = request.data['country']
            pro.save()
            pro_ser = ProfileSerializer(pro, many=False)
            return Response(pro_ser.data)
        pro = Profile.objects.create(
            user = request.user,
            phone = request.data['phone'],
            address = request.data['address'],
            city = request.data['city'],
            country = request.data['country']
        )
        pro_ser = ProfileSerializer(pro, many=False)
        return Response(pro_ser.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated,])
def MyShopcart(request):
    cart = ShopCart.objects.filter(user = request.user)
    serializers = ShopcartSerializer(cart, many=True)
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
    pro = Product.objects.get(id = request.data['id'])
    shopcart = ShopCart(
        product = pro,
        user = request.user,
        quantity = request.data['quantity']
    )
    shopcart.save()
    if Wishlist.objects.filter(product__id = request.POST['id'], user = request.user).exists():
        Wishlist.objects.get(product__id = request.POST['id'], user = request.user).delete()
    serializers = ShopcartSerializer(shopcart, many=False)
    return Response(serializers.data)

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
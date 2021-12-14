from django.shortcuts import render, redirect
from home.models import ShopInfo
from product.models import Category

from django.contrib.auth.models import User
from django.contrib.auth.models import User, auth
from django.contrib import messages

def Account(request):
    if request.method == "POST":
        if 'first_name' in request.POST:
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            email = request.POST['email']
            password = request.POST['password']

            user = User.objects.create_user(username = email, first_name = first_name, last_name = last_name, email = email)
            user.set_password(password)
            user.save()
            return redirect(request.path_info)
        else:
            email = request.POST['email']
            password = request.POST['password']
            user = auth.authenticate(username=email, password=password)

            if user is not None:
                auth.login(request, user)
                return redirect('/')
            else:
                messages.error(request, 'Invalid username or password!')
                return redirect(request.path_info)
                
    shopinfo = ShopInfo.objects.all().first()
    categorys = Category.objects.all()
    context={
        'shopinfo': shopinfo,
        'category': categorys
    }
    return render(request, 'account/login-register.html', context)

def Logout(request):
    auth.logout(request)
    return redirect('/')
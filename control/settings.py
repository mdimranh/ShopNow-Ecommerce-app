from django.shortcuts import render, redirect
from product.models import Product, Category
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from allauth.socialaccount.models import SocialApp

def SettingView(request):
    if request.method == 'POST':

        if 'facebook-app-id' in request.POST:
            if SocialApp.objects.filter(provider = 'facebook').exists():
                social_app = SocialApp.objects.get(provider = 'facebook')
                social_app.client_id = request.POST['facebook-app-id']
                social_app.secret = request.POST['facebook-app-secret']
                social_app.status = True if request.POST.get('facebook-enable') == 'on' else False
                social_app.save()
            else:
                social_app = SocialApp(
                    provider = 'facebook',
                    name='facebook',
                    client_id = request.POST['facebook-app-id'],
                    secret = request.POST['facebook-app-secret'],
                    status = True
                )
                social_app.save()
            return redirect(request.path_info)

        elif 'google-app-id' in request.POST:
            if SocialApp.objects.filter(provider = 'google').exists():
                social_app = SocialApp.objects.get(provider = 'google')
                social_app.client_id = request.POST['google-app-id']
                social_app.secret = request.POST['google-app-secret']
                social_app.status = True if request.POST.get('google-enable') == 'on' else False
                social_app.save()
            else:
                social_app = SocialApp(
                    provider = 'google',
                    name = 'google',
                    client_id = request.POST['google-app-id'],
                    secret = request.POST['google-app-secret'],
                    status = True
                )
                social_app.save()
            return redirect(request.path_info)

    facebook_login = SocialApp.objects.filter(name = 'facebook').first()
    google_login = SocialApp.objects.filter(name = 'google').first()
    context = {
        "facebook_login": facebook_login,
        "google_login": google_login,
        "setting_sec": True,
    }
    return render(request, "control/settings.html", context)
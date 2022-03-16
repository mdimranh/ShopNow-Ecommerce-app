from django.shortcuts import render, redirect
from product.models import Product, Category
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from allauth.socialaccount.models import SocialApp
import pytz

from setting.models import Slider, Slide, SiteFront, SiteConfiguration, Pages, Banner

from order.models import ShippingMethod

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

        elif 'free-label' in request.POST:
            id = request.POST['id']
            if id != 'null' and ShippingMethod.objects.filter(id = id).exists():
                shipping_method = ShippingMethod.objects.get(id = id)
                shipping_method.name = request.POST['free-label']
                shipping_method.fee = request.POST['free-amount']
                shipping_method.active = True if request.POST.get('free-shipping-enable') == 'on' else False
                shipping_method.save()
            else:
                shipping_method = ShippingMethod(
                    name = request.POST['free-label'],
                    fee = request.POST['free-amount'],
                    method_type= 'free',
                    active = True if request.POST.get('free-shipping-enable') == 'on' else False
                )
                shipping_method.save()
            return redirect(request.path_info)

        elif 'local-label' in request.POST:
            id = request.POST['id']
            if id != 'null' and ShippingMethod.objects.filter(id = id).exists():
                shipping_method = ShippingMethod.objects.get(id = id)
                shipping_method.name = request.POST['local-label']
                shipping_method.fee = request.POST['local-cost']
                shipping_method.active = True if request.POST.get('local-shipping-enable') == 'on' else False
                shipping_method.save()
            else:
                shipping_method = ShippingMethod(
                    name = request.POST['local-label'],
                    fee = request.POST['local-cost'],
                    method_type= 'local',
                    active = True if request.POST.get('local-shipping-enable') == 'on' else False
                )
                shipping_method.save()
            return redirect(request.path_info)

    facebook_login = SocialApp.objects.filter(name = 'facebook').first()
    google_login = SocialApp.objects.filter(name = 'google').first()
    free_shipping = ShippingMethod.objects.filter(method_type="free").first()
    local_shipping = ShippingMethod.objects.filter(method_type="local").first()
    context = {
        "facebook_login": facebook_login,
        "google_login": google_login,
        "free_shipping": free_shipping,
        "local_shipping": local_shipping,
        'timezones': pytz.all_timezones,
        "setting_sec": True,
    }
    return render(request, "control/settings.html", context)


def Sliders(request):
    if request.method == 'POST':
        name = request.POST["name"]
        speed = request.POST["speed"]
        autoplay = True if request.POST.get("autoplay", False) == 'on' else False
        autoplay_speed = request.POST["autoplay-speed"]
        dots = True if request.POST.get("dots", False) == 'on' else False
        arrows = True if request.POST.get("arrows", False) == 'on' else False
        new_slider = Slider(
            name = name,
            speed = speed,
            autoplay = autoplay,
            autoplay_timeout = autoplay_speed,
            dots = dots,
            arrows = arrows
        )
        new_slider.save()
        for i in range (len(request.FILES.getlist("thumbnail"))):
            cap1 = request.POST.getlist("caption1")[i] if len(request.POST.getlist("caption1")[i]) > 0 else ''
            cap2 = request.POST.getlist("caption2")[i] if len(request.POST.getlist("caption2")[i]) > 0 else ''
            cap3 = request.POST.getlist("caption3")[i] if len(request.POST.getlist("caption3")[i]) > 0 else ''
            calltotext = request.POST.getlist("calltotext")[i] if len(request.POST.getlist("calltotext")[i]) > 0 else ''
            calltourl = request.POST.getlist("calltourl")[i] if len(request.POST.getlist("calltourl")[i]) > 0 else ''
            openinnew = True if request.POST.get("open", False) == 'on' else False
            enable = True if request.POST.get("enable", False) == 'on' else False
            image = request.FILES.getlist("thumbnail")[i]
            new_slide = Slide(
                slider = new_slider,
                caption_1 = cap1,
                caption_2 = cap2,
                caption_3 = cap3,
                action_text = calltotext,
                action_url=calltourl,
                link_type=openinnew,
                image = image,
                active = enable,
                position=i+1
            )
            new_slide.save()
        return redirect(request.path_info)
    slider = Slider.objects.all()
    context = {
        "slider": slider,
        'onaction': SiteFront.objects.all().first(),
        'slider_sec': True,
        'slider_list_sec': True
    }
    return render(request, "control/slider.html", context)

def SliderDetails(request, id):
    if request.method == 'POST':
        change = request.POST["pos"].split(',')
        new_thumb = request.FILES.getlist("thumbnail")
        slide = Slider.objects.get(id = id)
        ids = request.POST.getlist("id")
        for sld in slide.slide.all():
            if str(sld.id) not in ids:
                sld.delete()
        p=1
        n=0 
        for sld_id in ids:
            if sld_id == 'new':
                cap1 = request.POST.getlist("caption1")[n] if len(request.POST.getlist("caption1")[n]) > 0 else ''
                cap2 = request.POST.getlist("caption2")[n] if len(request.POST.getlist("caption2")[n]) > 0 else ''
                cap3 = request.POST.getlist("caption3")[n] if len(request.POST.getlist("caption3")[n]) > 0 else ''
                calltotext = request.POST.getlist("calltotext")[n] if len(request.POST.getlist("calltotext")[n]) > 0 else ''
                calltourl = request.POST.getlist("calltourl")[n] if len(request.POST.getlist("calltourl")[n]) > 0 else ''
                openinnew = True if request.POST.get("open", False) == 'on' else False
                enable = True if request.POST.get("enable", False) == 'on' else False
                image = request.FILES.getlist("thumbnail")[n]
                new_slide = Slide(
                    slider = slide,
                    caption_1 = cap1,
                    caption_2 = cap2,
                    caption_3 = cap3,
                    action_text = calltotext,
                    action_url=calltourl,
                    link_type=openinnew,
                    image = new_thumb[change.index(str(p-1))],
                    active = enable,
                    position=p
                )
                new_slide.save()
                p+=1
                n+=1
            else:
                get_slide = Slide.objects.filter(id = sld_id).first()
                get_slide.position = p
                if str(p-1) in change:
                    get_slide.image = new_thumb[change.index(str(p-1))]
                get_slide.save()
                p+=1
        return redirect(request.path_info)
    slide = Slider.objects.get(id = id)
    context = {
        'slide': slide,
        'slider_sec': True,
        'slider_list_sec': True
    }
    return render(request, "control/slider.html", context)

def PageList(request):
    if request.method == "POST":
        page = Pages(
            name = request.POST['name'],
            body = request.POST['body'],
            active = True if request.POST.get("active") == 'on' else False
        )
        page.save()
        return redirect(request.path_info)
    allpage = Pages.objects.all()
    context = {
        'pages': allpage,
        'page_sec': True,
    }
    return render(request, "control/pages.html", context)

def PageDetails(request, id):
    if request.method == "POST":
        page = Pages.objects.get(id = request.POST['id'])
        page.name = request.POST['name']
        page.body = request.POST['body']
        page.active = True if request.POST.get("active") == 'on' else False
        page.save()
        allpage = Pages.objects.all()
        context = {
            'pages': allpage,
            'page_sec': True,
        }
        return render(request, "control/pages.html", context)
    page = Pages.objects.get(id = id)
    context = {
        'page': page,
        'page_sec': True,
    }
    return render(request, "control/pages.html", context)



def SiteFrontView(request):
    if request.method == 'POST':
        site_config = SiteConfiguration.objects.all().first()
        if 'name' in request.POST:
            site_config.name = request.POST['name']
            site_config.address = request.POST['address']
            site_config.save()
            site_front = SiteFront.objects.get()
            site_front.slider = Slider.objects.get(id = request.POST['slider'])
            site_config.save()
            return redirect(request.path_info)
        if request.FILES['logo']:
            print("-------------")
            site_config.logo = request.FILES.get('logo')
            site_config.favicon = request.FILES.get('favicon')
            site_config.save()
            return redirect(request.path_info)
    siteinfo = SiteConfiguration.objects.get()
    sliders = Slider.objects.all()
    all_page = Pages.objects.all().exclude(active = False)
    banners = Banner.objects.all().exclude(active = False)
    context = {
        "siteinfo": siteinfo,
        'sliders': sliders,
        'pages': all_page,
        'banners': banners,
        'slider_sec': True,
        'sitefront_sec': True
    }
    return render(request, "control/sitefront.html", context)
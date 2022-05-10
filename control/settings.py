from django.shortcuts import render, redirect
from django.http import JsonResponse
from product.models import Product, Category
from django.views import View
from django.views.generic import ListView
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from allauth.socialaccount.models import SocialApp
import pytz

from django_countries import countries

import json
import os

from setting.models import *

from order.models import ShippingMethod, PaymentMethod
from region.models import *

def SettingView(request):
	if request.method == 'POST':

		if 'support-countries' in request.POST:
			for c, d in countries:
				print(c, d)
			return redirect(request.path_info)

		elif 'facebook-app-id' in request.POST:
			if SocialApp.objects.filter(provider = 'facebook').exists():
				social_app = SocialApp.objects.get(provider = 'facebook')
				social_app.client_id = request.POST['facebook-app-id']
				social_app.secret = request.POST['facebook-app-secret']
				social_app.save()
			else:
				social_app = SocialApp(
					provider = 'facebook',
					name='facebook',
					client_id = request.POST['facebook-app-id'],
					secret = request.POST['facebook-app-secret']
				)
				social_app.save()
			return redirect(request.path_info)

		elif 'google-app-id' in request.POST:
			if SocialApp.objects.filter(provider = 'google').exists():
				social_app = SocialApp.objects.get(provider = 'google')
				social_app.client_id = request.POST['google-app-id']
				social_app.secret = request.POST['google-app-secret']
				social_app.save()
			else:
				social_app = SocialApp(
					provider = 'google',
					name = 'google',
					client_id = request.POST['google-app-id'],
					secret = request.POST['google-app-secret']
				)
				social_app.save()
			return redirect(request.path_info)

		elif 'free-label' in request.POST:
			if ShippingMethod.objects.filter(method_type = 'free').exists():
				shipping_method = ShippingMethod.objects.get(method_type = 'free')
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
			if ShippingMethod.objects.filter(method_type = 'local').exists():
				shipping_method = ShippingMethod.objects.get(method_type = 'local')
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

		elif 'paypal-client-id' in request.POST:
			payment_method, create = PaymentMethod.objects.get_or_create(
				name = 'paypal',
			)
			payment_method.client_id = request.POST['paypal-client-id']
			payment_method.secret = request.POST['paypal-secret']
			payment_method.active = True if request.POST.get('paypal-enable') == 'on' else False
			payment_method.save()
			return redirect(request.path_info)

		elif 'cashon-enable' in request.POST:
			payment_method, create = PaymentMethod.objects.get_or_create(
				name = 'cashon',
			)
			payment_method.active = True if request.POST.get('cashon-enable') == 'on' else False
			payment_method.about = request.POST['about-cashon']
			payment_method.save()
			return redirect(request.path_info)

		elif 'support-currency' in request.POST:
			data = open(os.path.join(settings.BASE_DIR, 'static/control/currency.json'), encoding='utf-8').read()
			data1 = json.loads(data)
			for cur in data1:
				if data1[cur]['code'] in request.POST.get('support-currency'):
					if not Currency.objects.filter(code = data1[cur]['code']).exists():
						crncy = Currency(
							symbol = data1[cur]['symbol'],
							name = data1[cur]['name'],
							symbol_native = data1[cur]['symbol_native'],
							decimal_digits = data1[cur]['decimal_digits'],
							code = data1[cur]['code'],
							name_plural = data1[cur]['name_plural']
						)
						crncy.save()
			# setting = Settings.objects.get()
			# setting.default_currency = Currency.objects.get(code = request.POST['default-currency'])
			# setting.save()
			return redirect(request.path_info)

		# elif 'mail-host' in request.POST:
		# 	email_config = EmailConfig.objects.get()
		# 	email_config.email_host = request.POST['mail-host']
		# 	email_config.email_port = request.POST['mail-port']
		# 	email_config.email_host_user = request.POST['mail-username']
		# 	email_config.email_host_password = request.POST['mail-password']
		# 	email_config.email_host_use = request.POST['encrypt']
		# 	email_config.save()
		# 	return redirect(request.path_info)

		# elif 'store-phone' in request.POST:
		# 	sinfo = StoreInfo.objects.get()
		# 	sinfo.phone = request.POST['store-phone']
		# 	sinfo.email = request.POST['store-email']
		# 	sinfo.address1 = request.POST['store-address1']
		# 	sinfo.tagline = request.POST['store-tagline']
		# 	sinfo.city = request.POST['store-city']
		# 	sinfo.country = request.POST['store-country']
		# 	sinfo.state = request.POST['store-state']
		# 	sinfo.zip = request.POST['store-zip']
		# 	try:
		# 		sinfo.address2 = request.POST['store-address2']
		# 	except:
		# 		pass

		# 	sinfo.save()
		# 	return redirect(request.path_info)

	facebook_login = SocialApp.objects.filter(name = 'facebook').first()
	google_login = SocialApp.objects.filter(name = 'google').first()
	free_shipping = ShippingMethod.objects.filter(method_type="free").first()
	local_shipping = ShippingMethod.objects.filter(method_type="local").first()
	paypal = PaymentMethod.objects.filter(name="paypal").first()
	cashon = PaymentMethod.objects.filter(name="cashon").first()
	data = open(os.path.join(settings.BASE_DIR, 'static/control/currency.json'), encoding='utf-8').read()
	data1 = json.loads(data)
	sup_currency = Currency.objects.values_list('code', flat=True)
	# for a in data1:
	#     print(data1[a]['symbol'])
	context = {
		"facebook_login": facebook_login,
		"google_login": google_login,
		"free_shipping": free_shipping,
		"local_shipping": local_shipping,
		'paypal': paypal,
		'cashon': cashon,
		'timezones': pytz.all_timezones,
		'currencies': data1,
		'sup_currency': sup_currency,
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
		# 'onaction': SiteConfiguration.objects.get(),
		'appearance_sec': True,
		'slider_list_sec': True
	}
	return render(request, "control/slider.html", context)

def SliderDetails(request, id):
	if request.method == 'POST':
		try:
			change = request.POST["pos"].split(',')
		except:
			change = []
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
		'appearance_sec': True,
		'slider_list_sec': True
	}
	return render(request, "control/slider.html", context)


class Banners(View):
	def get(self, request):
		all_banner = Banner.objects.all()
		context = {
			"banners": all_banner,
			'appearance_sec': True,
			'banner_list_sec': True
		}
		return render(request, 'control/banner.html', context)

	def post(self, request):
		active = True if request.POST.get('enable') == 'on' else False
		image = request.FILES.get("thumbnail")
		bnr = Banner(
			title=request.POST['name'],
			caption1=request.POST['caption1'], 
			caption2=request.POST['caption2'], 
			caption3=request.POST['caption3'],
			call_to_text=request.POST['calltotext'], 
			call_to_url=request.POST['calltourl'],
			image = image,
			active=active
		)
		bnr.save()
		return redirect(request.path_info)

class BannerDetails(View):
	def get(self, request, id):
		bnr = Banner.objects.get(id = id)
		context = {
			"banner": bnr,
			'appearance_sec': True,
			'edit_banner_sec': True
		}
		return render(request, 'control/banner.html', context)

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


class DeletePage(View):
	def post(self, request):
		total_page = len(request.POST["pages"].split(','))
		for page_id in request.POST["pages"].split(','):
			Pages.objects.get(id = page_id).delete()
		context = {
			'total' : total_page
		}
		return JsonResponse(context)


def SiteFrontView(request):
	# if request.method == 'POST':
	# 	site_config = SiteConfiguration.objects.get()
	# 	if 'name' in request.POST:
	# 		site_config.name = request.POST['name']
	# 		site_config.address = request.POST['address']
	# 		site_config.slider = Slider.objects.get(id = request.POST['slider'])
	# 		site_config.save()
	# 		return redirect(request.path_info)
	# 	elif 'logo' in request.FILES:
	# 		site_config.logo = request.FILES.get('logo')
	# 		site_config.favicon = request.FILES.get('favicon')
	# 		site_config.save()
	# 		return redirect(request.path_info)
	# 	# lst = [request.POST.get('banner[%d]' % i) for i in range(0, len(request.POST))]
	# 	elif 'banner1' in request.POST:
	# 		if len(request.POST['banner1']) > 0:
	# 			site_config.banner1 = Banner.objects.filter(id = request.POST['banner1']).first()
	# 		if len(request.POST['banner2']) > 0:
	# 			site_config.banner2 = Banner.objects.filter(id = request.POST['banner2']).first()
	# 		if len(request.POST['banner3']) > 0:
	# 			site_config.banner3 = Banner.objects.filter(id = request.POST['banner3']).first()
	# 		if len(request.POST['banner4']) > 0:
	# 			site_config.banner4 = Banner.objects.filter(id = request.POST['banner4']).first()
	# 		if len(request.POST['banner5']) > 0:
	# 			site_config.banner5 = Banner.objects.filter(id = request.POST['banner5']).first()
	# 		if len(request.POST['banner6']) > 0:
	# 			site_config.banner6 = Banner.objects.filter(id = request.POST['banner6']).first()
	# 		if len(request.POST['banner7']) > 0:
	# 			site_config.banner7 = Banner.objects.filter(id = request.POST['banner7']).first()
	# 		if len(request.POST['banner8']) > 0:
	# 			site_config.banner8 = Banner.objects.filter(id = request.POST['banner8']).first()
	# 		site_config.save()
	# 		return redirect(request.path_info)

	# 	elif 'title1' in request.POST:
	# 		ftr = Feature.objects.get()
	# 		ftr.title1 = request.POST['title1']
	# 		ftr.title2 = request.POST['title2']
	# 		ftr.title3 = request.POST['title3']
	# 		ftr.title4 = request.POST['title4']
	# 		ftr.subtitle1 = request.POST['subtitle1']
	# 		ftr.subtitle2 = request.POST['subtitle2']
	# 		ftr.subtitle3 = request.POST['subtitle3']
	# 		ftr.subtitle4 = request.POST['subtitle4']
	# 		ftr.icon1 = request.POST['icon1']
	# 		ftr.icon2 = request.POST['icon2']
	# 		ftr.icon3 = request.POST['icon3']
	# 		ftr.icon4 = request.POST['icon4']
	# 		ftr.save()
	# 		return redirect(request.path_info)

	# 	elif 'facebook-link' in request.POST:
	# 		site_config.facebook = request.POST['facebook-link']
	# 		site_config.twitter = request.POST['twitter']
	# 		site_config.youtube = request.POST['youtube']
	# 		site_config.instagram = request.POST['instagram']
	# 		site_config.save()
	# 		return redirect(request.path_info)

	# 	elif 'link' and 'title' in request.POST:
	# 		titles = request.POST.getlist('title')
	# 		lnks = request.POST.getlist('link')
	# 		if 'useful-link' in request.POST:
	# 			flinks, create = FooterLinks.objects.get_or_create(section_name = 'useful')
	# 			flinks.links.all().delete()
	# 			c = 0
	# 			for title in titles:
	# 				create_link = Links(
	# 					name=title,
	# 					link=lnks[0]
	# 				)
	# 				create_link.save()
	# 				flinks.links.add(create_link)
	# 				c += 1
	# 		else:
	# 			flinks, create = FooterLinks.objects.get_or_create(section_name = 'service')
	# 			flinks.links.all().delete()
	# 			c = 0
	# 			for title in titles:
	# 				create_link = Links(
	# 					name=title,
	# 					link=lnks[c]
	# 				)
	# 				create_link.save()
	# 				flinks.links.add(create_link)
	# 				c += 1

	# 		return redirect(request.path_info)

	# 	elif 'caro-name' in request.POST:
	# 		if len(request.POST['id']) == 0:
	# 			enable = True if request.POST.get("caro-enable", False) == 'on' else False
	# 			carousel = ProductCarousel(
	# 				name = request.POST['caro-name'],
	# 				enable = enable
	# 			)
	# 			if ProductCarousel.objects.all().count() > 0:
	# 				position = ProductCarousel.objects.all().count() + 1
	# 			else:
	# 				position = 1
	# 			carousel.position = position
	# 			carousel.save()
	# 			if request.POST.getlist('caro-category')[0].split(',')[0] != '':
	# 				for i in request.POST.getlist('caro-category')[0].split(','):
	# 					carousel.categories.add(Category.objects.get(id = i))
	# 			if request.POST.getlist('caro-group')[0].split(',')[0] != '':
	# 				for i in request.POST.getlist('caro-group')[0].split(','):
	# 					carousel.groups.add(Group.objects.get(id = i))
	# 			if request.POST.getlist('caro-subcategory')[0].split(',')[0] != '':
	# 				for i in request.POST.getlist('caro-subcategory')[0].split(','):
	# 					carousel.subcategorys.add(Subcategory.objects.get(id = i))
	# 			carousel.save()
				
	# 		else:
	# 			get_carousel = ProductCarousel.objects.get(id = request.POST['id'])
	# 			get_carousel.enable = True if request.POST.get("caro-enable") == 'on' else False
	# 			get_carousel.name = request.POST['caro-name']
	# 			get_carousel.save()
	# 			get_carousel.categories.clear()
	# 			get_carousel.groups.clear()
	# 			get_carousel.subcategorys.clear()
	# 			for i in request.POST.getlist('caro-category')[0].split(','):
	# 				get_carousel.categories.add(Category.objects.get(id = i))
	# 			if request.POST.getlist('caro-group')[0].split(',')[0] != '':
	# 				for i in request.POST.getlist('caro-group')[0].split(','):
	# 					get_carousel.groups.add(Group.objects.get(id = i))
	# 			if request.POST.getlist('caro-subcategory')[0].split(',')[0] != '':
	# 				for i in request.POST.getlist('caro-subcategory')[0].split(','):
	# 					get_carousel.subcategorys.add(Subcategory.objects.get(id = i))
	# 			get_carousel.save()
	# 		return redirect(request.path_info)

	# siteinfo = SiteConfiguration.objects.get()
	# useful_links, create = FooterLinks.objects.get_or_create(section_name = 'useful')
	# service_links, create = FooterLinks.objects.get_or_create(section_name = 'service')
	# sliders = Slider.objects.all()
	# all_page = Pages.objects.all().exclude(active = False)
	# banners = Banner.objects.all().exclude(active = False)
	# pro_caro = ProductCarousel.objects.all()
	# categorys = Category.objects.all()
	# groups = Group.objects.all()
	# subcategories = Subcategory.objects.all()
	# context = {
	# 	"siteinfo": siteinfo,
	# 	'sliders': sliders,
	# 	'pages': all_page,
	# 	'banners': banners,
	# 	'pro_caro': pro_caro,
	# 	'categorys': categorys,
	# 	'groups': groups,
	# 	'subcategories': subcategories,
	# 	'useful_links': useful_links,
	# 	'service_links': service_links,
	# 	'appearance_sec': True,
	# 	'sitefront_sec': True
	# }
	return render(request, "control/sitefront.html")

class CarouselUpdate(View):
	def post(self, request):
		carousel_id = request.POST['carousel_id'].split(',')
		if request.POST["action"] == 'update':
			p = 1
			for id in carousel_id:
				get_carousel = ProductCarousel.objects.get(id = id)
				get_carousel.position = p
				get_carousel.save()
				p+=1
			context = {
				"msg": "updated",
				"id": carousel_id
			}
			return JsonResponse(context)
		else:
			get_carousel = ProductCarousel.objects.get(id = request.POST['carousel_id'])
			get_carousel.delete()
			context = {
				"id": carousel_id,
				"msg": "deleted",
			}
			return JsonResponse(context)
			

class AreaView(View):
	def get(self, request):
		countries = Country.objects.all()
		context = {
			'countries': countries,
			'localization_sec': True,
			'area_sec': True,
		}
		return render(request, 'control/area.html', context)

	def post(self, request):
		type = request.POST['type'] 
		if type == 'add-country':
			enable = True if request.POST.get('enable') == 'on' else False
			Country.objects.get_or_create(name = request.POST['name'], enable = enable)
		elif type == 'add-region':
			enable = True if request.POST.get('enable') == 'on' else False
			get_country = Country.objects.get(id = request.POST['id'])
			Region.objects.get_or_create(name = request.POST['name'], country=get_country, enable = enable)
		elif type == 'add-city':
			enable = True if request.POST.get('enable') == 'on' else False
			get_region = Region.objects.get(id = request.POST['id'])
			City.objects.get_or_create(name = request.POST['name'], region=get_region, enable = enable)
		elif type == 'add-area':
			enable = True if request.POST.get('enable') == 'on' else False
			get_city = City.objects.get(id = request.POST['id'])
			Area.objects.get_or_create(name = request.POST['name'], city=get_city, enable = enable)
		elif type == 'edit-country':
			enable = True if request.POST.get('enable') == 'on' else False
			get_country = Country.objects.get(id = request.POST['id'])
			get_country.name = request.POST['name']
			get_country.enable = enable
			get_country.save()
		elif type == 'edit-region':
			enable = True if request.POST.get('enable') == 'on' else False
			get_region = Region.objects.get(id = request.POST['id'])
			get_region.name = request.POST['name']
			get_region.enable = enable
			get_region.save()
		elif type == 'edit-city':
			enable = True if request.POST.get('enable') == 'on' else False
			get_city = City.objects.get(id = request.POST['id'])
			get_city.name = request.POST['name']
			get_city.enable = enable
			get_city.save()
		elif type == 'edit-area':
			enable = True if request.POST.get('enable') == 'on' else False
			get_area = Area.objects.get(id = request.POST['id'])
			get_area.enable = enable
			get_area.save()
		return redirect(request.path_info)

class CurrencyList(ListView):
	model = Currency
	template_name='control/currency.html'
	context_object_name = 'currencies'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['localization_sec'] = True
		context['currency_sec'] = True
		return context

class CurrencyView(View):
	def get(self, request, id):
		get_currency = Currency.objects.get(id = id)
		context = {
			'currency': get_currency,
			'localization_sec': True,
			'currency_sec': True,
		}
		return render(request, 'control/currency.html', context)
	
	def post(self, request, id):
		get_currency = Currency.objects.get(id = id)
		get_currency.name = request.POST['name']
		get_currency.name_plural = request.POST['name_plural']
		get_currency.code = request.POST['code']
		get_currency.symbol = request.POST['symbol']
		get_currency.symbol_native = request.POST['symbol_native']
		get_currency.rate = request.POST['rate']
		get_currency.request = request
		get_currency.save()
		return redirect(request.path_info)

import json
class LocalizationDelete(View):
	def post(self, request):
		data = json.loads(request.POST['info'])['data']
		for i in data:
			if i[0] == 'country':
				Country.objects.get(id = i[1]).delete()
			elif i[0] == 'region':
				Region.objects.get(id = i[1]).delete()
			elif i[0] == 'city':
				City.objects.get(id = i[1]).delete()
			elif i[0] == 'area':
				Area.objects.get(id = i[1]).delete()
		return JsonResponse({'msg': 'success'})
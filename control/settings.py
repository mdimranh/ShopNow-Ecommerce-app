from django.shortcuts import render
from product.models import Product, Category
from django.core.files.storage import FileSystemStorage
from django.conf import settings

def SettingView(request):
    context = {
        "setting_sec": True,
    }
    return render(request, "control/settings.html", context)
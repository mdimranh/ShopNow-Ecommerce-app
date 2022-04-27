from django.conf import settings
from django.conf.urls.static import static

from django.conf import urls

from django.contrib import admin
from django.urls import path, include
import home

urlpatterns = [
    path('control', include('control.urls')),
    path('admin', admin.site.urls),
    path('', include('home.urls')),
    path('', include('product.urls')),
    path('', include('accounts.urls')),
    path('', include('order.urls')),
    path('accounts/', include('allauth.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('api/', include('api.urls'))
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

from django.conf.urls import handler400

urls.handler400 = home.views.error_404
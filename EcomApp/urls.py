from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('control.urls')),
    path('admin/', admin.site.urls),
    path('', include('home.urls')),
    path('', include('product.urls')),
    path('', include('account.urls')),
    path('', include('order.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
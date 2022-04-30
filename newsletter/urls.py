from django.urls import path
from .views import AddNewsletterEmail

urlpatterns = [
    path('newsletter/add-email', AddNewsletterEmail.as_view())
]

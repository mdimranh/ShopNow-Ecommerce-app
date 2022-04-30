from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
from .models import NewsletterEmail

class AddNewsletterEmail(View):
    def post(self, request, *args, **kwargs):
        email = request.POST['email']
        if not NewsletterEmail.objects.filter(email = email).exists():
            nlemail = NewsletterEmail(
                email=email
            )
            nlemail.request = request
            nlemail.save()
            type = 'add'
            return JsonResponse({'type': type})
        else:
            type = 'exist'
            return JsonResponse({'type': type})

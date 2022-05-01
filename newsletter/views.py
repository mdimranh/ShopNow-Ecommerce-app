from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
from .models import NewsletterEmail

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site

# from setting.models import EmailConfig
# from control.emailconfig import backend

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
            try:
                return JsonResponse({'type': type})
            finally:
                email_config = EmailConfig.objects.get()
                subject, from_email, to = 'Welcome to newsletter', email_config.email_host_user, email
                text_content = 'Welcome to newsletter.'
                html_content = render_to_string('newsletter/welcome-newsletter.html', context={
                    'domain': get_current_site(request).domain
                })
                msg = EmailMultiAlternatives(subject, text_content, from_email, [to], connection=backend)
                msg.attach_alternative(html_content, "text/html")
                msg.send()
        else:
            type = 'exist'
            return JsonResponse({'type': type})

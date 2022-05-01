from django.shortcuts import render, redirect
from django.views.generic import View, ListView
from newsletter.models import NewsletterEmail, Newsletter

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site

from setting.models import EmailConfig
from control.emailconfig import backend

class NewsletterList(ListView):
    allow_empty = True
    model = Newsletter
    context_object_name = 'newsletters'
    template_name='control/newsletter.html'

    def get_context_data(self, **kwargs):
        context = super(NewsletterList, self).get_context_data(**kwargs)
        context['newsletter_sec'] = True
        return context

class AddNewsletter(View):
    def post(self, request, *args, **kwargs):
        try:
            return redirect('/control/newsletter')
        finally:
            email_config = EmailConfig.objects.all().first()
            subject, from_email, to = request.POST['subject'], email_config.email_host_user, list(NewsletterEmail.objects.all().values_list('email', flat=True))
            text_content = request.POST['subject']
            html_content = str(request.POST['body'])
            msg = EmailMultiAlternatives(subject, text_content, from_email, to, connection=backend)
            msg.attach_alternative(html_content, "text/html")
            msg.send()

            nl = Newsletter(
                subject=request.POST['subject'],
                body=request.POST['body'],
                emails=to
            )
            nl.save()

class NewsletterDetails(View):
    def get(self, request, id, *args, **kwargs):
        get_newsletter = Newsletter.objects.get(id = id)
        context = {
            'newsletter': get_newsletter,
            'newsletter_sec' : True
        }
        return render(request, 'control/newsletter.html', context)
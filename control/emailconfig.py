from django.core.mail import EmailMessage
from django.core.mail.backends.smtp import EmailBackend

from setting.models import EmailConfig

config = EmailConfig.objects.get()

backend = EmailBackend(
        host=config.email_host,
        port=config.email_port,
        username=config.email_host_user,
        password=config.email_host_password,
        use_tls=True,
        fail_silently=True
    )
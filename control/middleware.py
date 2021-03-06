from django.utils.deprecation import MiddlewareMixin
from django.urls import resolve, reverse
from django.http import HttpResponseRedirect
from EcomApp import settings
from django.contrib.sites.shortcuts import get_current_site
from django.contrib import messages


class LoginRequireMidleware(MiddlewareMixin):
    def process_request(self, request):
        # assert hasattr(request, 'user')
        # current_route_name = resolve(request.path_info).url_name
        # if not current_route_name in settings.AUTH_EXEMPT_ROUTES:
        #     return HttpResponseRedirect(reverse(settings.AUTH_LOGIN_ROUTE))
            

        path = request.path
        if path.startswith("/control") and not path.startswith("/control/login"):
            if not request.user.is_authenticated:
                return HttpResponseRedirect(reverse(settings.AUTH_LOGIN_ROUTE))
            else:
                if not request.user.is_superuser and not request.user.is_staff:
                    # return HttpResponseRedirect(reverse(settings.ROOT_URL))
                    messages.error(request, "You haven't permission to access admin panel.")
                    return render('control/login.html')
        
from django.utils.deprecation import MiddlewareMixin
from django.conf import settings
from django.http import HttpResponseForbidden

class DisableCSRFForCertainHosts(MiddlewareMixin):
    def process_request(self, request):
        # Список хостов, для которых нужно отключить CSRF
        allowed_hosts = ['http://localhost:5173']

        # Проверяем, есть ли текущий хост в списке разрешённых
        if request.get_host() in allowed_hosts:
            # Убираем проверку CSRF
            setattr(request, '_dont_enforce_csrf_checks', True)
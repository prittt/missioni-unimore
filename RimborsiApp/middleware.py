from django.shortcuts import reverse, redirect
from django.conf import settings


class MaintenanceModeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.META.get('PATH_INFO', "")
        query = request.META.get('QUERY_STRING', "")

        if settings.MAINTENANCE_BYPASS_QUERY in query:
            request.session['bypass_maintenance'] = True

        if not request.session.get('bypass_maintenance', False):
            if settings.MAINTENANCE_MODE and path != reverse("RimborsiApp:maintenance"):
                response = redirect(reverse("RimborsiApp:maintenance"))
                return response

        response = self.get_response(request)

        return response
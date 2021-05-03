from django.conf import settings


class VersionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        header = settings.VERSION_CODE_HEADER
        if header:
            version = settings.VERSION_CODE
            response[header] = version
        return response

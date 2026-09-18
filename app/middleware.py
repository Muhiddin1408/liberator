from django.conf import settings
from django.utils import translation


class AdminUzbekMiddleware:
    """Admin panel doim o'zbek tilida ochiladi (brauzer tilidan qat'i nazar).

    LocaleMiddleware'dan keyin turishi kerak: u tilni brauzer/cookie bo'yicha
    tanlaydi, bu middleware esa admin manzillari uchun uni "uz" ga almashtiradi.
    """

    def __init__(self, get_response):
        self.get_response = get_response
        self.admin_prefix = "/" + settings.ADMIN_URL

    def __call__(self, request):
        if request.path.startswith(self.admin_prefix):
            translation.activate("uz")
            request.LANGUAGE_CODE = "uz"
        return self.get_response(request)

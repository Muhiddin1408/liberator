from urllib.parse import urlparse

from django.conf import settings
from django.http import HttpResponsePermanentRedirect
from django.utils import translation


class CanonicalHostMiddleware:
    """www.liberator.uz -> liberator.uz (301): Google bitta saytni ikki domenda ko'rmasligi uchun.

    Asosiy domen SITE_URL dan olinadi. Faqat uning www'li (yoki www'siz) juftligi yo'naltiriladi.
    """

    def __init__(self, get_response):
        self.get_response = get_response
        host = urlparse(settings.SITE_URL).netloc
        self.alias = host[4:] if host.startswith("www.") else "www." + host

    def __call__(self, request):
        if request.method in ("GET", "HEAD") and request.META.get("HTTP_HOST", "").lower() == self.alias:
            return HttpResponsePermanentRedirect(settings.SITE_URL + request.get_full_path())
        return self.get_response(request)


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

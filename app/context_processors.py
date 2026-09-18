from django.conf import settings
from django.core.cache import cache
from django.urls import reverse, translate_url
from django.utils.translation import get_language

from app import seo
from app.forms import CallbackForm
from app.models import ServiceCategory, SiteSettings

MENU_CACHE_KEY = "menu_categories"


def menu_categories():
    categories = cache.get(MENU_CACHE_KEY)
    if categories is None:
        categories = list(ServiceCategory.objects.active())
        cache.set(MENU_CACHE_KEY, categories, 60 * 15)
    return categories


def site_context(request):
    """Har bir sahifada kerak bo'ladigan umumiy ma'lumotlar (menyu, kontaktlar, SEO)."""
    path = request.path
    current = (get_language() or settings.LANGUAGE_CODE)[:2]
    alternates = [
        {"code": code, "name": name, "url": translate_url(path, code), "active": code == current}
        for code, name in settings.LANGUAGES
    ]
    site = SiteSettings.load()
    return {
        "site": site,
        "org_schema": seo.legal_service(site, settings.SITE_URL + reverse("index")),
        "menu_categories": menu_categories(),
        "current_lang": current,
        "language_alternates": alternates,
        "site_url": settings.SITE_URL,
        "canonical_url": settings.SITE_URL + path,
        "x_default_url": settings.SITE_URL + translate_url(path, settings.LANGUAGE_CODE),
        "callback_form": CallbackForm(initial={"source_page": path}, auto_id="cb_%s"),
        "YANDEX_METRIKA_ID": settings.YANDEX_METRIKA_ID,
        "GOOGLE_ANALYTICS_ID": settings.GOOGLE_ANALYTICS_ID,
        "TAWK_TO_ID": settings.TAWK_TO_ID,
        "GOOGLE_SITE_VERIFICATION": settings.GOOGLE_SITE_VERIFICATION,
        "YANDEX_VERIFICATION": settings.YANDEX_VERIFICATION,
    }

from django.conf import settings
from django.core.cache import cache
from django.urls import reverse, translate_url
from django.utils.translation import get_language, override

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


def language_versions(request):
    """Joriy sahifaning har tildagi manzili va shu tilda to'liq tarjima qilinganmi.

    Obyekt sahifalarida (xizmat, maqola, advokat) slug tilga qarab o'zgaradi, shuning uchun
    manzil obyektning o'zidan olinadi. Boshqa sahifalar uchun Django'ning translate_url yetarli.
    """
    obj = getattr(request, "i18n_object", None)
    versions = []
    for code, name in settings.LANGUAGES:
        if obj is not None:
            with override(code):
                url = obj.get_absolute_url()
            available = obj.has_language(code) if hasattr(obj, "has_language") else True
        else:
            url, available = translate_url(request.path, code), True
        versions.append({"code": code, "name": name, "url": url, "available": available})
    return versions


def site_context(request):
    """Har bir sahifada kerak bo'ladigan umumiy ma'lumotlar (menyu, kontaktlar, SEO)."""
    path = request.path
    current = (get_language() or settings.LANGUAGE_CODE)[:2]
    versions = language_versions(request)
    for version in versions:
        version["active"] = version["code"] == current
    default = next(v for v in versions if v["code"] == settings.LANGUAGE_CODE)
    current_version = next((v for v in versions if v["active"]), None)
    site = SiteSettings.load()
    return {
        "site": site,
        "org_schema": seo.legal_service(site, settings.SITE_URL + reverse("index")),
        "menu_categories": menu_categories(),
        "current_lang": current,
        # Til almashtirgich hamma tilni ko'rsatadi; hreflang esa faqat tarjimasi borlarini.
        "language_alternates": versions,
        "hreflang_versions": [v for v in versions if v["available"]],
        # Tarjimasi yo'q sahifa o'zbekcha matnni ko'rsatadi — Google uni dublikat deb hisoblamasligi uchun.
        "noindex": bool(current_version and not current_version["available"]),
        "site_url": settings.SITE_URL,
        "canonical_url": settings.SITE_URL + path,
        "x_default_url": settings.SITE_URL + default["url"],
        "callback_form": CallbackForm(initial={"source_page": path}, auto_id="cb_%s"),
        "YANDEX_METRIKA_ID": settings.YANDEX_METRIKA_ID,
        "GOOGLE_ANALYTICS_ID": settings.GOOGLE_ANALYTICS_ID,
        "TAWK_TO_ID": settings.TAWK_TO_ID,
        "GOOGLE_SITE_VERIFICATION": settings.GOOGLE_SITE_VERIFICATION,
        "YANDEX_VERIFICATION": settings.YANDEX_VERIFICATION,
    }

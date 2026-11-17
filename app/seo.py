"""SEO: sahifa sarlavhasi/tavsifi va Schema.org (JSON-LD) tuzilmalari."""
import html
import re

from django.conf import settings
from django.templatetags.static import static
from django.utils.html import strip_tags
from django.utils.text import Truncator
from django.utils.translation import get_language

BRAND = "Liberator"
TITLE_LIMIT = 60
ALTERNATE_NAMES = [
    "Liberator advokatlik firmasi", "Liberator advokatura",
    "Адвокатская фирма Liberator", "Адвокатура Liberator",
    "Liberator Law Firm",
]
KEYWORDS = (
    "advokat, advokatura, advokatlik firmasi, yurist, "
    "адвокат, адвокатура, адвокатская фирма, юрист, "
    "law firm, lawyer, attorney, advocate, advokatura"
)  # Google natijalarida sarlavha taxminan shu uzunlikda kesiladi
DESCRIPTION_LIMIT = 158


def plain_text(value):
    """HTML (CKEditor) matnini meta teglar uchun oddiy bir qatorli matnga aylantiradi."""
    return re.sub(r"\s+", " ", html.unescape(strip_tags(str(value or "")))).strip()


def page_title(*candidates):
    """Sig'adigan eng to'liq sarlavhani tanlaydi: avval brend bilan, sig'masa brendsiz.

    `candidates` — eng to'liqdan eng qisqagacha: ("Xizmat — Yo'nalish", "Xizmat").
    """
    candidates = [plain_text(c) for c in candidates if c]
    for title in candidates:
        if len(f"{title} | {BRAND}") <= TITLE_LIMIT:
            return f"{title} | {BRAND}"
    for title in candidates:
        if len(title) <= TITLE_LIMIT:
            return title
    return candidates[-1] if candidates else BRAND


def page_description(*candidates, suffix=""):
    """Birinchi bo'sh bo'lmagan matndan 158 belgigacha tavsif. Qisqa bo'lsa `suffix` qo'shiladi."""
    for candidate in candidates:
        text = plain_text(candidate)
        if not text:
            continue
        if suffix and len(text) + len(suffix) + 1 <= DESCRIPTION_LIMIT:
            if text[-1] not in ".!?…":
                text += "."
            return f"{text} {suffix}"
        return Truncator(text).chars(DESCRIPTION_LIMIT)
    return ""


def organization_ref():
    return {"@id": settings.SITE_URL + "/#organization"}


def absolute(url):
    if not url:
        return ""
    return url if url.startswith("http") else settings.SITE_URL + url


def legal_service(site, url):
    data = {
        "@context": "https://schema.org",
        "@type": "LegalService",
        "@id": settings.SITE_URL + "/#organization",
        "name": "Liberator",
        "alternateName": ALTERNATE_NAMES,
        "url": url,
        "logo": absolute(static("site/img/logo.png")),
        "image": absolute(static("site/img/og-image.jpg")),
        "description": site.tr("meta_description"),
        "keywords": KEYWORDS,
        "telephone": site.phone_primary,
        "email": site.email,
        "hasMap": site.map_link,
        "knowsLanguage": ["uz", "ru", "en"],
        "contactPoint": [{
            "@type": "ContactPoint",
            "telephone": phone,
            "contactType": "customer service",
            "areaServed": "UZ",
            "availableLanguage": ["Uzbek", "Russian", "English"],
        } for phone in site.phones],
        "areaServed": [{"@type": "City", "name": "Tashkent"}, {"@type": "Country", "name": "Uzbekistan"}],
        "address": {
            "@type": "PostalAddress",
            "streetAddress": site.tr("address"),
            "addressLocality": "Tashkent",
            "addressCountry": "UZ",
        },
        "geo": {"@type": "GeoCoordinates", "latitude": float(site.latitude), "longitude": float(site.longitude)},
        "openingHoursSpecification": [{
            "@type": "OpeningHoursSpecification",
            "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"],
            "opens": "09:00",
            "closes": "18:00",
        }],
    }
    same_as = [u for u in (site.telegram_url, site.instagram_url, site.facebook_url,
                           site.youtube_url, site.linkedin_url) if u]
    if same_as:
        data["sameAs"] = same_as
    return data


def website():
    """Bosh sahifa uchun: Google natijalarida sayt nomi to'g'ri ko'rinishi uchun."""
    return {
        "@context": "https://schema.org",
        "@type": "WebSite",
        "@id": settings.SITE_URL + "/#website",
        "name": BRAND,
        "alternateName": ALTERNATE_NAMES,
        "url": settings.SITE_URL + "/",
        "inLanguage": [code for code, _name in settings.LANGUAGES],
        "publisher": organization_ref(),
    }


def service(name, description, url, service_type=""):
    """Xizmat yo'nalishi yoki alohida xizmat sahifasi."""
    data = {
        "@context": "https://schema.org",
        "@type": "Service",
        "name": name,
        "url": absolute(url),
        "provider": organization_ref(),
        "areaServed": {"@type": "Country", "name": "Uzbekistan"},
    }
    if service_type:
        data["serviceType"] = service_type
    if plain_text(description):
        data["description"] = Truncator(plain_text(description)).chars(300)
    return data


def person(staff):
    data = {
        "@context": "https://schema.org",
        "@type": "Person",
        "name": staff.localized_full_name,
        "jobTitle": staff.localized_position,
        "url": absolute(staff.get_absolute_url()),
        "worksFor": organization_ref(),
    }
    if staff.image_url:
        data["image"] = absolute(staff.image_url)
    if staff.localized_short_description:
        data["description"] = staff.localized_short_description
    if staff.localized_specialization:
        data["knowsAbout"] = Truncator(plain_text(staff.localized_specialization)).chars(300)
    same_as = [u for u in (staff.linkedin, staff.telegram) if u]
    if same_as:
        data["sameAs"] = same_as
    return data


def article(news):
    data = {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": news.tr("title")[:110],
        "datePublished": news.published_at.isoformat(),
        "dateModified": news.updated_at.isoformat(),
        "mainEntityOfPage": absolute(news.get_absolute_url()),
        "inLanguage": (get_language() or settings.LANGUAGE_CODE)[:2],
        "publisher": organization_ref(),
        "image": absolute(news.image.url if news.image else static("site/img/og-image.jpg")),
    }
    description = page_description(news.tr("summary"), news.tr("body"))
    if description:
        data["description"] = description
    if news.author:
        data["author"] = {"@type": "Person", "name": news.author.localized_full_name,
                          "url": absolute(news.author.get_absolute_url())}
    else:
        data["author"] = organization_ref()
    return data


def faq_page(faqs):
    return faq_pairs([(faq.tr("question"), faq.tr("answer")) for faq in faqs])


def faq_pairs(pairs):
    """FAQPage sxemasi: pairs — (savol, javob) juftliklari."""
    return {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [{
            "@type": "Question",
            "name": str(question),
            "acceptedAnswer": {"@type": "Answer", "text": str(answer)},
        } for question, answer in pairs],
    }


def breadcrumbs(items):
    """items: [(nom, url), ...]"""
    return {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": i, "name": name, "item": absolute(url)}
            for i, (name, url) in enumerate(items, start=1)
        ],
    }

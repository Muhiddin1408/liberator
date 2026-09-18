"""Schema.org (JSON-LD) tuzilmalari — Google qidiruv natijalarida boy ko'rinish uchun."""
from django.conf import settings
from django.templatetags.static import static
from django.utils.html import strip_tags


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
        "alternateName": "“LIBERATOR” advokatlik firmasi",
        "url": url,
        "logo": absolute(static("site/img/logo.png")),
        "image": absolute(static("site/img/og-image.jpg")),
        "description": site.tr("meta_description"),
        "telephone": site.phone_primary,
        "email": site.email,
        "foundingDate": str(site.founded_year),
        "areaServed": {"@type": "Country", "name": "Uzbekistan"},
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


def person(staff):
    data = {
        "@context": "https://schema.org",
        "@type": "Person",
        "name": staff.localized_full_name,
        "jobTitle": staff.localized_position,
        "url": absolute(staff.get_absolute_url()),
        "worksFor": {"@id": settings.SITE_URL + "/#organization"},
    }
    if staff.image_url:
        data["image"] = absolute(staff.image_url)
    if staff.localized_specialization:
        data["knowsAbout"] = strip_tags(staff.localized_specialization)[:300]
    return data


def article(news):
    data = {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": news.tr("title")[:110],
        "datePublished": news.published_at.isoformat(),
        "dateModified": news.updated_at.isoformat(),
        "mainEntityOfPage": absolute(news.get_absolute_url()),
        "publisher": {"@id": settings.SITE_URL + "/#organization"},
    }
    if news.image:
        data["image"] = absolute(news.image.url)
    if news.author:
        data["author"] = {"@type": "Person", "name": news.author.localized_full_name,
                          "url": absolute(news.author.get_absolute_url())}
    return data


def faq_page(faqs):
    return {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [{
            "@type": "Question",
            "name": faq.tr("question"),
            "acceptedAnswer": {"@type": "Answer", "text": faq.tr("answer")},
        } for faq in faqs],
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

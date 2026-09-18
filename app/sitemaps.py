from urllib.parse import urlparse

from django.conf import settings
from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from app.models import News, Service, ServiceCategory, Staff


class BaseSitemap(Sitemap):
    # Har bir sahifa uch tilda: /uz/, /ru/, /en/ + hreflang alternates.
    i18n = True
    alternates = True
    x_default = True
    protocol = urlparse(settings.SITE_URL).scheme or "https"


class StaticSitemap(BaseSitemap):
    priority = 0.8
    changefreq = "monthly"

    def items(self):
        return ["index", "about", "team", "service_list", "news_list", "contact"]

    def location(self, item):
        return reverse(item)


class ServiceCategorySitemap(BaseSitemap):
    priority = 0.9
    changefreq = "monthly"

    def items(self):
        return ServiceCategory.objects.active()


class ServiceSitemap(BaseSitemap):
    priority = 0.7
    changefreq = "monthly"

    def items(self):
        return Service.objects.active().filter(category__is_active=True).select_related("category")


class StaffSitemap(BaseSitemap):
    priority = 0.6
    changefreq = "monthly"

    def items(self):
        return Staff.objects.filter(is_active=True)

    def lastmod(self, obj):
        return obj.updated_at


class NewsSitemap(BaseSitemap):
    priority = 0.6
    changefreq = "weekly"

    def items(self):
        return News.objects.published()

    def lastmod(self, obj):
        return obj.updated_at


sitemaps = {
    "static": StaticSitemap,
    "services": ServiceCategorySitemap,
    "service-items": ServiceSitemap,
    "team": StaffSitemap,
    "news": NewsSitemap,
}

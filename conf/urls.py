from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path, re_path
from django.views.generic import RedirectView

from app import views
from app.sitemaps import sitemaps

admin.site.site_header = "Liberator — boshqaruv"
admin.site.site_title = "Liberator Admin"
admin.site.index_title = "Boshqaruv paneli"

urlpatterns = [
    path(settings.ADMIN_URL, admin.site.urls),
    path("ckeditor5/", include("django_ckeditor_5.urls")),
    path("i18n/", include("django.conf.urls.i18n")),
    path("sitemap.xml", sitemap, {"sitemaps": sitemaps}, name="sitemap"),
    path("robots.txt", views.robots_txt, name="robots_txt"),
    re_path(r"^mailru-domain(?P<code>[A-Za-z0-9]+)\.html$", views.mailru_verification),
    path("favicon.ico", RedirectView.as_view(url=settings.STATIC_URL + "site/img/favicon.ico", permanent=True)),

    # Eski manzillar (tilsiz, pk bilan) — Google'dagi havolalar yo'qolmasin.
    path("service/<int:pk>", views.legacy_service_redirect),
    path("contact", RedirectView.as_view(pattern_name="contact", permanent=True)),
    path("about/", RedirectView.as_view(pattern_name="about", permanent=True)),
    path("team/", RedirectView.as_view(pattern_name="team", permanent=True)),
    path("team/<slug:slug>/", RedirectView.as_view(pattern_name="team_detail", permanent=True)),
]

# /uz/..., /ru/..., /en/... — har bir til alohida indekslanadi.
urlpatterns += i18n_patterns(
    path("", include("app.urls")),
    prefix_default_language=True,
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

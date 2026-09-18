from django.urls import path
from django.utils.text import format_lazy
from django.utils.translation import pgettext_lazy

from app import views
from app.models import LegalPage


# URL bo'laklari har tilda o'zicha: /uz/xizmatlar/, /ru/uslugi/, /en/services/.
# Tarjimasi locale/*/django.po da ("URL" kontekstida).
urlpatterns = [
    path("", views.index, name="index"),
    path(pgettext_lazy("URL", "biz-haqimizda/"), views.about, name="about"),
    path(pgettext_lazy("URL", "jamoa/"), views.TeamListView.as_view(), name="team"),
    path(format_lazy("{}<slug:slug>/", pgettext_lazy("URL", "jamoa/")), views.TeamDetailView.as_view(), name="team_detail"),
    path(pgettext_lazy("URL", "xizmatlar/"), views.service_list, name="service_list"),
    path(format_lazy("{}<slug:slug>/", pgettext_lazy("URL", "xizmatlar/")), views.service_category, name="service_category"),
    path(format_lazy("{}<slug:category_slug>/<slug:slug>/", pgettext_lazy("URL", "xizmatlar/")),
         views.service_detail, name="service_detail"),
    path(pgettext_lazy("URL", "maqolalar/"), views.NewsListView.as_view(), name="news_list"),
    path(format_lazy("{}<slug:slug>/", pgettext_lazy("URL", "maqolalar/")), views.news_detail, name="news_detail"),
    path(pgettext_lazy("URL", "aloqa/"), views.contact, name="contact"),
    path(pgettext_lazy("URL", "maxfiylik-siyosati/"), views.legal_page, {"kind": LegalPage.PRIVACY}, name="privacy"),
    path(pgettext_lazy("URL", "foydalanish-shartlari/"), views.legal_page, {"kind": LegalPage.TERMS}, name="terms"),
    # Texnik sahifalar (indekslanmaydi) — hamma tilda bir xil.
    path("murojaat/", views.lead_submit, name="lead_submit"),
    path("rahmat/", views.thanks, name="thanks"),
]

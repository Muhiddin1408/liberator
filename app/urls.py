from django.urls import path

from app import views
from app.models import LegalPage

urlpatterns = [
    path("", views.index, name="index"),
    path("biz-haqimizda/", views.about, name="about"),
    path("jamoa/", views.TeamListView.as_view(), name="team"),
    path("jamoa/<slug:slug>/", views.TeamDetailView.as_view(), name="team_detail"),
    path("xizmatlar/", views.service_list, name="service_list"),
    path("xizmatlar/<slug:slug>/", views.service_category, name="service_category"),
    path("xizmatlar/<slug:category_slug>/<slug:slug>/", views.service_detail, name="service_detail"),
    path("yangiliklar/", views.NewsListView.as_view(), name="news_list"),
    path("yangiliklar/<slug:slug>/", views.NewsDetailView.as_view(), name="news_detail"),
    path("aloqa/", views.contact, name="contact"),
    path("murojaat/", views.lead_submit, name="lead_submit"),
    path("rahmat/", views.thanks, name="thanks"),
    path("maxfiylik-siyosati/", views.legal_page, {"kind": LegalPage.PRIVACY}, name="privacy"),
    path("foydalanish-shartlari/", views.legal_page, {"kind": LegalPage.TERMS}, name="terms"),
]

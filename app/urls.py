from django.urls import path

from app.views import (
    DashboardView,
    about,
    TeamListView,
    TeamDetailView,
    contact,
    service,
    set_language_from_url,
)

urlpatterns = [
    path('', DashboardView.as_view(), name='index'),
    path('about/', about, name='about'),
    path('team/', TeamListView.as_view(), name='terms'),
    path('team/<slug:slug>/', TeamDetailView.as_view(), name='team_detail'),
    path('contact', contact, name='contact'),
    path('service/<int:pk>', service, name='service'),
    path('change-language/<str:lang_code>/', set_language_from_url, name='change_lang'),
]

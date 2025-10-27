from django.contrib import admin
from django.urls import path

from app.views import DashboardView, about, Teams, contact, service, set_language_from_url

urlpatterns = [
    path('', DashboardView.as_view(), name='index'),
    path('about/', about, name='about'),
    path('terms/', Teams.as_view(), name='terms'),
    path('contact', contact, name='contact'),
    path('service/<int:pk>', service, name='service'),
    path('change-language/<str:lang_code>/', set_language_from_url, name='change_lang')
]
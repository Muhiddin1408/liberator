import re

from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView

from app.models import Staff, Service, ServiceCategory


# Create your views here.


class DashboardView(TemplateView):
    template_name = 'index.html'
    def get(self, request, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['services'] = ServiceCategory.objects.all()

        return render(request, 'index.html', context)


def about(request):
    services = ServiceCategory.objects.all()
    return render(request, 'about.html', {"services": services})


class Teams(TemplateView):
    template_name = 'team.html'
    def get(self, request, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['staffs'] = Staff.objects.all()
        return render(request, "team.html", context)

def contact(request):
    services = ServiceCategory.objects.all()
    return render(request, 'contact.html', {"services": services})
def service(request, pk):
    service = Service.objects.filter(category_id=pk)
    service_category = ServiceCategory.objects.all()
    services = ServiceCategory.objects.all()
    image = ServiceCategory.objects.get(pk=pk).image
    return render(request, "service_item.html", {"service": service, "service_category": service_category, "image": image, "services": services})

from django.shortcuts import redirect
from django.utils.translation import activate
from django.conf import settings


def set_language_from_url(request, lang_code):
    if lang_code in [lang[0] for lang in settings.LANGUAGES]:
        activate(lang_code)
        request.session['django_language'] = lang_code

    next_url = request.META.get('HTTP_REFERER', '/')
    return redirect(next_url)

from django.shortcuts import redirect
from django.utils.translation import activate
from django.conf import settings
from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView, ListView, DetailView

from app.models import Staff, Service, ServiceCategory, Partner


class DashboardView(TemplateView):
    template_name = 'index.html'

    def get(self, request, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['services'] = ServiceCategory.objects.all()
        return render(request, 'index.html', context)


def about(request):
    services = ServiceCategory.objects.all()
    partner = Partner.objects.all()
    return render(request, 'about.html', {"services": services, "partners": partner})


class TeamListView(ListView):
    model = Staff
    template_name = "team.html"
    context_object_name = "staffs"

    def get_queryset(self):
        return Staff.objects.filter(is_active=True).order_by("order", "id")

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["services"] = ServiceCategory.objects.all()
        return ctx


class TeamDetailView(DetailView):
    model = Staff
    template_name = "team_detail.html"
    context_object_name = "staff"
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def get_queryset(self):
        return Staff.objects.filter(is_active=True)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["services"] = ServiceCategory.objects.all()
        ctx["other_staffs"] = (
            Staff.objects.filter(is_active=True)
            .exclude(pk=self.object.pk)
            .order_by("order", "id")[:3]
        )
        return ctx


def contact(request):
    services = ServiceCategory.objects.all()
    return render(request, 'contact.html', {"services": services})


def service(request, pk):
    category = get_object_or_404(ServiceCategory, pk=pk)
    service_qs = Service.objects.filter(category_id=pk)
    service_category = ServiceCategory.objects.all()
    services = ServiceCategory.objects.all()
    return render(
        request,
        "service_item.html",
        {
            "service": service_qs,
            "service_category": service_category,
            "image": category.image,
            "services": services,
        },
    )


def set_language_from_url(request, lang_code):
    if lang_code in [lang[0] for lang in settings.LANGUAGES]:
        activate(lang_code)
        request.session['django_language'] = lang_code

    next_url = request.META.get('HTTP_REFERER', '/')
    return redirect(next_url)

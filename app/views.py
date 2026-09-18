import logging

from django.conf import settings
from django.contrib import messages
from django.core.cache import cache
from django.db.models import Q
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.translation import get_language
from django.utils.translation import gettext as _
from django.views.decorators.cache import cache_control
from django.views.decorators.http import require_GET, require_POST
from django.views.generic import DetailView, ListView

from app import seo
from app.forms import CallbackForm, ConsultationForm
from app.models import (
    FAQ, Achievement, ConsultationRequest, LegalPage, News, Partner, Service, ServiceCategory, Staff, Testimonial,
)
from app.notifications import notify_new_lead
from app.utils import client_ip

logger = logging.getLogger(__name__)


def published_testimonials():
    return Testimonial.objects.filter(is_published=True, consent_received=True)


def consultation_form(request, **initial):
    initial.setdefault("source_page", request.path)
    return ConsultationForm(initial=initial)


def get_translated(queryset, slug):
    """Obyektni joriy til slug'i bo'yicha topadi.

    Boshqa tildagi slug bilan kelinsa (masalan /ru/uslugi/korporativ-huquq/), obyekt baribir topiladi —
    view uni to'g'ri manzilga 301 bilan yo'naltiradi.
    """
    lang = (get_language() or "uz")[:2]
    field = "slug" if lang == "uz" else f"slug_{lang}"
    obj = queryset.filter(**{field: slug}).first()
    if obj is None:
        obj = queryset.filter(Q(slug=slug) | Q(slug_ru=slug) | Q(slug_en=slug)).first()
    if obj is None:
        raise Http404
    return obj


def mark_translated_page(request, obj):
    """Context processor shu obyekt bo'yicha hreflang va noindex'ni hisoblaydi."""
    request.i18n_object = obj


# --- Sahifalar ------------------------------------------------------------------

def index(request):
    return render(request, "index.html", {
        "achievements": Achievement.objects.active(),
        "testimonials": published_testimonials(),
        "latest_news": News.objects.published().select_related("author")[:3],
        "team": Staff.objects.filter(is_active=True).order_by("order", "id")[:4],
        "form": consultation_form(request),
    })


def about(request):
    return render(request, "about.html", {
        "partners": Partner.objects.active(),
        "achievements": Achievement.objects.active(),
        "testimonials": published_testimonials(),
    })


class TeamListView(ListView):
    template_name = "team.html"
    context_object_name = "staffs"

    def get_queryset(self):
        return Staff.objects.filter(is_active=True).order_by("order", "id")


class TeamDetailView(DetailView):
    template_name = "team_detail.html"
    context_object_name = "staff"

    def get_queryset(self):
        return Staff.objects.filter(is_active=True)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        mark_translated_page(self.request, self.object)
        ctx["other_staffs"] = (
            Staff.objects.filter(is_active=True).exclude(pk=self.object.pk).order_by("order", "id")[:3]
        )
        ctx["articles"] = self.object.articles.published()[:3]
        ctx["form"] = consultation_form(self.request, staff=self.object.pk)
        ctx["schema"] = seo.person(self.object)
        return ctx


def service_list(request):
    return render(request, "service_list.html", {
        "categories": ServiceCategory.objects.active(),
    })


def service_category(request, slug):
    category = get_translated(ServiceCategory.objects.active(), slug)
    if category.get_absolute_url() != request.path:
        return redirect(category.get_absolute_url(), permanent=True)
    mark_translated_page(request, category)
    faqs = list(category.faqs.active())
    return render(request, "service_category.html", {
        "category": category,
        "services": category.services.active(),
        "faqs": faqs,
        "faq_schema": seo.faq_page(faqs) if faqs else None,
        "form": consultation_form(request, service=category.pk),
    })


def service_detail(request, category_slug, slug):
    service = get_translated(
        Service.objects.active().select_related("category").filter(category__is_active=True), slug,
    )
    if service.get_absolute_url() != request.path:
        return redirect(service.get_absolute_url(), permanent=True)
    mark_translated_page(request, service)
    return render(request, "service_detail.html", {
        "service": service,
        "category": service.category,
        "siblings": service.category.services.active().exclude(pk=service.pk),
        "form": consultation_form(request, service=service.category_id),
    })


class NewsListView(ListView):
    template_name = "news_list.html"
    context_object_name = "articles"
    paginate_by = 9

    def get_queryset(self):
        return News.objects.published().select_related("author")


def news_detail(request, slug):
    article = get_translated(News.objects.published().select_related("author"), slug)
    if article.get_absolute_url() != request.path:
        return redirect(article.get_absolute_url(), permanent=True)
    mark_translated_page(request, article)
    return render(request, "news_detail.html", {
        "article": article,
        "recent": News.objects.published().exclude(pk=article.pk)[:3],
        "schema": seo.article(article),
        "form": consultation_form(request),
    })


def contact(request):
    faqs = list(FAQ.objects.active().filter(category__isnull=True))
    return render(request, "contact.html", {
        "form": consultation_form(request),
        "faqs": faqs,
        "faq_schema": seo.faq_page(faqs) if faqs else None,
    })


def legal_page(request, kind):
    page = LegalPage.objects.filter(kind=kind).first()
    if page is None:
        raise Http404
    return render(request, "legal_page.html", {"page": page})


def thanks(request):
    return render(request, "thanks.html")


# --- Murojaat qabul qilish ---------------------------------------------------------

def is_rate_limited(ip):
    if not ip:
        return False
    key = f"lead-rate:{ip}"
    if cache.add(key, 1, 60 * 60):
        return False
    try:
        count = cache.incr(key)
    except ValueError:
        cache.set(key, 1, 60 * 60)
        return False
    return count > settings.LEAD_RATE_LIMIT_PER_HOUR


@require_POST
def lead_submit(request):
    is_callback = request.POST.get("kind") == ConsultationRequest.KIND_CALLBACK
    form = (CallbackForm if is_callback else ConsultationForm)(request.POST)
    ip = client_ip(request)

    if form.is_valid():
        if is_rate_limited(ip):
            messages.error(request, _("Juda ko‘p so‘rov yuborildi. Iltimos, keyinroq urinib ko‘ring yoki "
                                      "bizga qo‘ng‘iroq qiling."))
            return redirect("contact")
        lead = form.save(commit=False)
        lead.language = (request.LANGUAGE_CODE or "")[:5]
        lead.ip_address = ip
        lead.save()
        logger.info("Yangi murojaat #%s (%s)", lead.pk, lead.kind)
        notify_new_lead(lead)
        return redirect("thanks")

    faqs = list(FAQ.objects.active().filter(category__isnull=True))
    return render(request, "contact.html", {"form": form, "faqs": faqs}, status=400)


# --- Texnik -----------------------------------------------------------------------

@require_GET
@cache_control(max_age=60 * 60 * 24)
def robots_txt(request):
    lines = [
        "User-agent: *",
        "Disallow: /i18n/",
        "Disallow: /ckeditor5/",
        "Disallow: /*/murojaat/",
        "Disallow: /*/rahmat/",
        "",
        f"Sitemap: {settings.SITE_URL}{reverse('sitemap')}",
        "",
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")


@require_GET
def mailru_verification(request, code):
    if not settings.MAILRU_VERIFICATION or code != settings.MAILRU_VERIFICATION:
        raise Http404
    return HttpResponse(f"mailru-domain: {code}", content_type="text/html")


def legacy_service_redirect(request, pk):
    category = get_object_or_404(ServiceCategory, pk=pk)
    return redirect(category.get_absolute_url(), permanent=True)

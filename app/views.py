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


def crumbs(*items):
    """BreadcrumbList sxemasi: Bosh sahifa > ... > joriy sahifa. items: (nom, url)."""
    return seo.breadcrumbs([(_("Bosh sahifa"), reverse("index")), *items])


def firm_suffix():
    return _("Liberator advokatlik firmasi, Toshkent. Bepul konsultatsiya.")


# --- Sahifalar ------------------------------------------------------------------

def advokatura_faq():
    """Bosh sahifadagi "Advokatura" bloki: ko'rinadigan matn va FAQPage sxemasi bir manbadan."""
    return [
        (_("Advokatura nima?"), _(
            "Advokatura — advokatlik faoliyati bilan shug‘ullanadigan shaxslarning mustaqil kasbiy birlashmalarini "
            "o‘z ichiga olgan huquqiy institut. Uning vazifasi — jismoniy va yuridik shaxslarga malakali yuridik "
            "yordam ko‘rsatish. O‘zbekistonda advokatlar advokatlik byurosi, advokatlik firmasi yoki advokatlar "
            "hay’atida ishlaydi; Liberator — advokatlik firmasi."
        )),
        (_("Advokat va yuristning farqi nima?"), _(
            "Advokat — malaka imtihonini topshirgan, litsenziya olgan va Advokatlar palatasiga a’zo bo‘lgan yurist. "
            "Jinoyat ishida himoyachi sifatida faqat advokat qatnashadi, mijoz bilan muloqoti esa advokatlik siri "
            "sifatida qonun bilan himoyalanadi."
        )),
        (_("Liberator advokaturasiga qanday murojaat qilish mumkin?"), _(
            "Saytdagi formani to‘ldiring, qo‘ng‘iroq qiling yoki Toshkentdagi ofisimizga keling. Birinchi "
            "konsultatsiya bepul: advokat vaziyatingizni o‘rganib, keyingi qadamlarni tushuntiradi. O‘zbek, rus va "
            "ingliz tillarida ishlaymiz."
        )),
    ]


def index(request):
    faq = advokatura_faq()
    return render(request, "index.html", {
        "meta_title": _("Advokat va advokatura Toshkentda — Liberator"),
        "schema": seo.website(),
        "advokatura_faq": faq,
        "faq_schema": seo.faq_pairs(faq),
        "achievements": Achievement.objects.active(),
        "testimonials": published_testimonials(),
        "latest_news": News.objects.published().select_related("author")[:3],
        "team": Staff.objects.filter(is_active=True).order_by("order", "id")[:4],
        "form": consultation_form(request),
    })


def about(request):
    return render(request, "about.html", {
        "meta_title": _("Liberator advokatlik firmasi haqida — Toshkent"),
        "meta_description": _(
            "Liberator — Toshkentdagi advokatlik firmasi: biznes va fuqarolarga yuridik hamrohlik, sudda vakillik "
            "va jinoyat ishlari bo‘yicha himoya."
        ),
        "breadcrumb_schema": crumbs((_("Biz haqimizda"), reverse("about"))),
        "partners": Partner.objects.active(),
        "achievements": Achievement.objects.active(),
        "testimonials": published_testimonials(),
    })


class TeamListView(ListView):
    template_name = "team.html"
    context_object_name = "staffs"

    def get_queryset(self):
        return Staff.objects.filter(is_active=True).order_by("order", "id")

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["meta_title"] = _("Advokatlar jamoasi — Liberator, Toshkent")
        ctx["meta_description"] = _(
            "Liberator advokatlik firmasining advokat va yuristlari: jinoyat, fuqarolik, iqtisodiy va ma’muriy "
            "ishlar bo‘yicha mutaxassislar. Mos advokatni tanlang."
        )
        ctx["breadcrumb_schema"] = crumbs((_("Bizning jamoa"), reverse("team")))
        return ctx


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
        staff = self.object
        ctx["schema"] = seo.person(staff)
        ctx["breadcrumb_schema"] = crumbs(
            (_("Bizning jamoa"), reverse("team")), (staff.localized_full_name, staff.get_absolute_url()),
        )
        headline = f"{staff.localized_full_name} — {staff.localized_position}"
        ctx["meta_title"] = seo.page_title(headline, staff.localized_full_name)
        ctx["meta_description"] = seo.page_description(
            _("%(headline)s, Liberator advokatlik firmasi (Toshkent). %(about)s") % {
                "headline": headline,
                "about": seo.plain_text(staff.localized_short_description or staff.localized_specialization),
            },
        )
        if staff.image_url:
            ctx["og_image"] = seo.absolute(staff.image_url)
        return ctx


def service_list(request):
    return render(request, "service_list.html", {
        "meta_title": _("Yuridik xizmatlar va advokat yordami Toshkentda | Liberator"),
        "meta_description": _(
            "Toshkentda advokat xizmatlari: jinoyat, fuqarolik, iqtisodiy va ma’muriy ishlar, biznesni yuridik "
            "hamrohlik qilish. Birinchi konsultatsiya bepul."
        ),
        "breadcrumb_schema": crumbs((_("Xizmatlar"), reverse("service_list"))),
        "categories": ServiceCategory.objects.active(),
    })


def service_category(request, slug):
    category = get_translated(ServiceCategory.objects.active(), slug)
    if category.get_absolute_url() != request.path:
        return redirect(category.get_absolute_url(), permanent=True)
    mark_translated_page(request, category)
    faqs = list(category.faqs.active())
    name, description = category.tr("name"), category.tr("description")
    return render(request, "service_category.html", {
        "meta_title": seo.page_title(_("%(name)s — advokat xizmatlari Toshkentda") % {"name": name}, name),
        "meta_description": seo.page_description(description, suffix=firm_suffix()),
        "og_image": seo.absolute(category.image.url) if category.image else "",
        "schema": seo.service(name, description, category.get_absolute_url()),
        "breadcrumb_schema": crumbs(
            (_("Xizmatlar"), reverse("service_list")), (name, category.get_absolute_url()),
        ),
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
    category = service.category
    title, category_name, description = service.tr("title"), category.tr("name"), service.tr("description")
    return render(request, "service_detail.html", {
        "meta_title": seo.page_title(f"{title} — {category_name}", title),
        "meta_description": seo.page_description(description, suffix=firm_suffix()),
        "schema": seo.service(title, description, service.get_absolute_url(), service_type=category_name),
        "breadcrumb_schema": crumbs(
            (_("Xizmatlar"), reverse("service_list")),
            (category_name, category.get_absolute_url()),
            (title, service.get_absolute_url()),
        ),
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

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        title = _("Huquqiy maqolalar va yangiliklar")
        number = ctx["page_obj"].number
        if number > 1:
            # Har bir sahifa o'zini canonical qiladi (1-sahifaga emas) — Google keyingi sahifalarni ham ko'radi.
            self.request.canonical_query = f"?page={number}"
            title = _("%(title)s — %(number)s-sahifa") % {"title": title, "number": number}
        ctx["meta_title"] = seo.page_title(title)
        ctx["meta_description"] = _(
            "Liberator advokatlarining amaliy maslahatlari: biznes, mehnat, soliq, oila va jinoyat huquqi "
            "bo‘yicha maqolalar hamda qonunchilikdagi muhim o‘zgarishlar."
        )
        ctx["breadcrumb_schema"] = crumbs((_("Maqolalar"), reverse("news_list")))
        return ctx


def news_detail(request, slug):
    article = get_translated(News.objects.published().select_related("author"), slug)
    if article.get_absolute_url() != request.path:
        return redirect(article.get_absolute_url(), permanent=True)
    mark_translated_page(request, article)
    return render(request, "news_detail.html", {
        "meta_title": seo.page_title(article.tr("title")),
        "meta_description": seo.page_description(article.tr("summary"), article.tr("body")),
        "og_image": seo.absolute(article.image.url) if article.image else "",
        "breadcrumb_schema": crumbs(
            (_("Maqolalar"), reverse("news_list")), (article.tr("title"), article.get_absolute_url()),
        ),
        "article": article,
        "recent": News.objects.published().exclude(pk=article.pk)[:3],
        "schema": seo.article(article),
        "form": consultation_form(request),
    })


def contact(request):
    faqs = list(FAQ.objects.active().filter(category__isnull=True))
    return render(request, "contact.html", {
        "meta_title": _("Advokat bilan bog‘lanish — bepul konsultatsiya | Liberator"),
        "meta_description": _(
            "Liberator advokatlik firmasi bilan bog‘laning: telefon, Telegram yoki onlayn ariza. "
            "Ofisimiz Toshkentda. Birinchi konsultatsiya bepul."
        ),
        "breadcrumb_schema": crumbs((_("Aloqa"), reverse("contact"))),
        "form": consultation_form(request),
        "faqs": faqs,
        "faq_schema": seo.faq_page(faqs) if faqs else None,
    })


def legal_page(request, kind):
    page = LegalPage.objects.filter(kind=kind).first()
    if page is None:
        raise Http404
    return render(request, "legal_page.html", {"page": page, "meta_title": seo.page_title(page.tr("title"))})


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


@require_GET
def yandex_verification(request, code):
    """Yandex Webmaster "HTML file" usuli: bosh manzil (/) tilga yo'naltirgani uchun meta teg usuli ishlamaydi."""
    if not settings.YANDEX_VERIFICATION or code != settings.YANDEX_VERIFICATION:
        raise Http404
    return HttpResponse(
        '<html><head><meta http-equiv="Content-Type" content="text/html; charset=UTF-8"></head>'
        f"<body>Verification: {code}</body></html>",
        content_type="text/html; charset=UTF-8",
    )


def legacy_service_redirect(request, pk):
    category = get_object_or_404(ServiceCategory, pk=pk)
    return redirect(category.get_absolute_url(), permanent=True)

import shutil
import tempfile
import time
from io import BytesIO
from unittest import mock

from django.conf import settings
from django.core import mail, signing
from django.core.cache import cache
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import reverse
from django.utils import translation
from PIL import Image

from app.forms import _signer
from app.models import ConsultationRequest, News, Service, ServiceCategory, SiteSettings, Staff, Testimonial


def old_token(seconds_ago=10):
    return _signer.sign(str(int(time.time()) - seconds_ago))


def lead_data(**extra):
    data = {
        "kind": "consultation",
        "full_name": "Ali Valiyev",
        "phone": "+998 90 123 45 67",
        "message": "Mehnat nizosi bo'yicha maslahat kerak",
        "consent": "on",
        "form_token": old_token(),
        "source_page": "/uz/aloqa/",
    }
    data.update(extra)
    return data


class PagesTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.category = ServiceCategory.objects.create(
            name="Korporativ huquq", name_ru="Корпоративное право", description="Tavsif", description_ru="Описание",
        )
        cls.service = Service.objects.create(category=cls.category, title="Due diligence")
        cls.staff = Staff.objects.create(full_name="Ali Valiyev", position="Advokat", position_ru="Адвокат")
        cls.news = News.objects.create(title="Mehnat shartnomasi", body="<p>Matn</p>", is_published=True,
                                       author=cls.staff)

    def test_all_pages_render_in_every_language(self):
        names = ["index", "about", "team", "service_list", "news_list", "contact", "privacy", "terms", "thanks"]
        for lang in ("uz", "ru", "en"):
            with translation.override(lang):
                urls = [reverse(n) for n in names] + [
                    self.category.get_absolute_url(), self.service.get_absolute_url(),
                    self.staff.get_absolute_url(), self.news.get_absolute_url(),
                ]
            for url in urls:
                with self.subTest(url=url):
                    self.assertTrue(url.startswith(f"/{lang}/"))
                    self.assertEqual(self.client.get(url).status_code, 200)

    def test_root_redirects_to_language_prefix(self):
        self.assertRedirects(self.client.get("/"), "/uz/", fetch_redirect_response=False)

    def test_russian_page_is_translated(self):
        response = self.client.get("/ru/kontakty/")
        self.assertContains(response, "Бесплатная консультация")
        self.assertContains(response, '<html lang="ru">')

    def test_seo_tags(self):
        response = self.client.get("/ru/o-nas/")
        self.assertContains(response, 'rel="canonical"')
        for code in ("uz", "ru", "en", "x-default"):
            self.assertContains(response, f'hreflang="{code}"')
        self.assertContains(response, 'property="og:image"')
        self.assertContains(response, '"@type": "LegalService"')

    def test_no_template_leftovers(self):
        for url in ("/uz/", "/uz/biz-haqimizda/"):
            content = self.client.get(url).content.decode()
            for leftover in ("bracketweb", "procounsel", "Lorem Ipsum", "Alen Martin", "Ronald Richards", "4.6", "5k+"):
                self.assertNotIn(leftover, content, f"{leftover!r} {url} sahifasida qolgan")

    def test_legacy_urls_redirect_permanently(self):
        response = self.client.get(f"/service/{self.category.pk}")
        self.assertEqual(response.status_code, 301)
        self.assertEqual(response["Location"], self.category.get_absolute_url())
        self.assertEqual(self.client.get("/contact").status_code, 301)

    def test_inactive_and_unpublished_hidden(self):
        self.category.is_active = False
        self.category.save()
        self.assertEqual(self.client.get(self.category.get_absolute_url()).status_code, 404)
        draft = News.objects.create(title="Qoralama", body="x", is_published=False)
        self.assertEqual(self.client.get(draft.get_absolute_url()).status_code, 404)

    def test_testimonial_needs_consent(self):
        Testimonial.objects.create(author_name="Maxfiy Mijoz", text="Zo'r", is_published=True, consent_received=False)
        self.assertNotContains(self.client.get("/uz/"), "Maxfiy Mijoz")

    def test_sitemap_and_robots(self):
        sitemap = self.client.get("/sitemap.xml")
        self.assertEqual(sitemap.status_code, 200)
        self.assertContains(sitemap, "/ru/uslugi/korporativnoe-pravo/")
        self.assertContains(sitemap, 'hreflang="en"')
        robots = self.client.get("/robots.txt")
        self.assertContains(robots, "Sitemap:")

    def test_slugs_generated(self):
        other = ServiceCategory.objects.create(name="Korporativ huquq!")
        self.assertEqual(self.category.slug, "korporativ-huquq")
        self.assertEqual(other.slug, "korporativ-huquq-2")


class MultilingualSeoTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.full = ServiceCategory.objects.create(
            name="Soliq huquqi", name_ru="Налоговое право", name_en="Tax law",
            description="Tavsif", description_ru="Описание", description_en="Description",
        )
        cls.partial = ServiceCategory.objects.create(name="Mehnat huquqi", description="Tavsif")

    def test_each_language_has_own_url_and_slug(self):
        self.assertEqual(self.full.slug_ru, "nalogovoe-pravo")
        with translation.override("ru"):
            self.assertEqual(self.full.get_absolute_url(), "/ru/uslugi/nalogovoe-pravo/")
        with translation.override("en"):
            self.assertEqual(self.full.get_absolute_url(), "/en/services/tax-law/")
        self.assertEqual(self.client.get("/en/services/tax-law/").status_code, 200)

    def test_wrong_language_slug_redirects_permanently(self):
        response = self.client.get("/ru/uslugi/soliq-huquqi/")
        self.assertEqual(response.status_code, 301)
        self.assertEqual(response["Location"], "/ru/uslugi/nalogovoe-pravo/")

    def test_hreflang_lists_all_translated_versions(self):
        html = self.client.get("/uz/xizmatlar/soliq-huquqi/").content.decode()
        self.assertIn('hreflang="ru" href="http://127.0.0.1:8000/ru/uslugi/nalogovoe-pravo/"', html.replace(
            settings.SITE_URL, "http://127.0.0.1:8000"))
        self.assertIn('hreflang="x-default"', html)
        self.assertNotIn("noindex", html)

    def test_untranslated_page_is_noindex_and_not_in_sitemap(self):
        response = self.client.get("/ru/uslugi/mehnat-huquqi/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<meta name="robots" content="noindex, follow">')
        self.assertNotContains(response, 'rel="alternate" hreflang=')
        sitemap = self.client.get("/sitemap.xml").content.decode()
        self.assertIn("/uz/xizmatlar/mehnat-huquqi/", sitemap)
        self.assertNotIn("/ru/uslugi/mehnat-huquqi/", sitemap)

    def test_translated_static_urls(self):
        for url in ("/ru/o-nas/", "/ru/komanda/", "/ru/stati/", "/ru/kontakty/", "/en/about/", "/en/contact/",
                    "/en/privacy-policy/", "/ru/politika-konfidentsialnosti/"):
            with self.subTest(url=url):
                self.assertEqual(self.client.get(url).status_code, 200)


@override_settings(LEAD_NOTIFY_EMAILS=["office@example.com"], TELEGRAM_BOT_TOKEN="", LEAD_RATE_LIMIT_PER_HOUR=3)
class LeadFormTests(TestCase):
    url = "/uz/murojaat/"

    def setUp(self):
        cache.clear()

    def test_valid_request_saved_and_notified(self):
        response = self.client.post(self.url, lead_data())
        self.assertRedirects(response, "/uz/rahmat/")
        lead = ConsultationRequest.objects.get()
        self.assertEqual(lead.status, "new")
        self.assertEqual(lead.language, "uz")
        self.assertEqual(lead.ip_address, "127.0.0.1")
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn("Ali Valiyev", mail.outbox[0].body)

    def test_callback_only_needs_name_and_phone(self):
        data = {k: v for k, v in lead_data(kind="callback").items() if k != "message"}
        self.assertRedirects(self.client.post(self.url, data), "/uz/rahmat/")
        self.assertEqual(ConsultationRequest.objects.get().kind, "callback")

    def test_honeypot_blocks_bots(self):
        response = self.client.post(self.url, lead_data(website="http://spam.example"))
        self.assertEqual(response.status_code, 400)
        self.assertFalse(ConsultationRequest.objects.exists())

    def test_too_fast_submission_rejected(self):
        response = self.client.post(self.url, lead_data(form_token=old_token(0)))
        self.assertEqual(response.status_code, 400)

    def test_forged_token_rejected(self):
        response = self.client.post(self.url, lead_data(form_token=signing.TimestampSigner().sign("1")))
        self.assertEqual(response.status_code, 400)

    def test_consent_and_phone_required(self):
        response = self.client.post(self.url, lead_data(consent="", phone="abc"))
        self.assertEqual(response.status_code, 400)
        self.assertIn("consent", response.context["form"].errors)
        self.assertIn("phone", response.context["form"].errors)

    def test_rate_limit(self):
        for _ in range(3):
            self.client.post(self.url, lead_data())
        response = self.client.post(self.url, lead_data())
        self.assertRedirects(response, "/uz/aloqa/")
        self.assertEqual(ConsultationRequest.objects.count(), 3)

    @override_settings(TELEGRAM_BOT_TOKEN="123:abc", TELEGRAM_CHAT_ID="42")
    def test_telegram_failure_does_not_lose_lead(self):
        with mock.patch("app.notifications.urllib.request.urlopen", side_effect=OSError("down")):
            response = self.client.post(self.url, lead_data())
        self.assertRedirects(response, "/uz/rahmat/")
        self.assertEqual(ConsultationRequest.objects.count(), 1)

    def test_get_not_allowed(self):
        self.assertEqual(self.client.get(self.url).status_code, 405)


class ModelTests(TestCase):
    def test_localized_fallback(self):
        category = ServiceCategory.objects.create(name="Soliq", name_en="Tax")
        with translation.override("en"):
            self.assertEqual(category.tr("name"), "Tax")
        with translation.override("ru"):
            self.assertEqual(category.tr("name"), "Soliq")

    def test_site_settings_singleton(self):
        first = SiteSettings.load()
        first.email = "new@example.com"
        first.save()
        SiteSettings(email="other@example.com").save()
        self.assertEqual(SiteSettings.objects.count(), 1)

    def test_uploaded_image_is_compressed_to_webp(self):
        media_root = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, media_root, True)
        buffer = BytesIO()
        Image.new("RGB", (3000, 2000), "white").save(buffer, "JPEG")
        upload = SimpleUploadedFile("photo.jpg", buffer.getvalue(), content_type="image/jpeg")
        with self.settings(MEDIA_ROOT=media_root):
            staff = Staff.objects.create(full_name="Rasm Test", position="Advokat", image=upload)
            self.assertTrue(staff.image.name.endswith(".webp"))
            with Image.open(staff.image.path) as img:
                self.assertLessEqual(max(img.size), 900)



class AdminLanguageTests(TestCase):
    def test_admin_is_uzbek_regardless_of_browser_language(self):
        response = self.client.get("/admin/login/", HTTP_ACCEPT_LANGUAGE="en-US,en;q=0.9")
        self.assertContains(response, "Kirish")
        self.assertContains(response, "Parol")

    def test_site_still_follows_url_language(self):
        response = self.client.get("/ru/kontakty/", HTTP_ACCEPT_LANGUAGE="en")
        self.assertContains(response, "Бесплатная консультация")


class ContentCommandTests(TestCase):
    def call(self, *args):
        from django.core.management import call_command

        call_command(*args, stdout=open("/dev/null", "w"))

    def test_seed_content_is_hidden_by_default(self):
        self.call("seed_content")
        self.assertEqual(ServiceCategory.objects.count(), 6)
        self.assertFalse(ServiceCategory.objects.filter(is_active=True).exists())
        self.assertFalse(News.objects.filter(is_published=True).exists())
        self.assertTrue(all(c.has_language("ru") and c.has_language("en") for c in ServiceCategory.objects.all()))

    def test_seed_content_never_overwrites_admin_text(self):
        category = ServiceCategory.objects.create(name="Korporativ huquq", description="Firma matni", is_active=True)
        self.call("seed_content")
        category.refresh_from_db()
        self.assertEqual(category.description, "Firma matni")  # o'zgarmadi
        self.assertTrue(category.description_ru)  # bo'sh tarjima to'ldirildi
        self.assertTrue(category.is_active)

    def test_seed_content_twice_creates_no_duplicates(self):
        self.call("seed_content", "--publish")
        self.call("seed_content", "--publish")
        self.assertEqual(ServiceCategory.objects.count(), 6)
        self.assertEqual(News.objects.count(), 4)
        response = self.client.get("/ru/stati/")
        self.assertContains(response, "Вызвали к следователю")

    def test_demo_data_clear_removes_only_fake_people(self):
        with self.settings(DEBUG=True, MEDIA_ROOT=tempfile.mkdtemp()):
            self.call("demo_data")
            self.assertEqual(Staff.objects.count(), 4)
            self.assertEqual(self.client.get("/uz/").status_code, 200)
            self.call("demo_data", "--clear")
        self.assertFalse(Staff.objects.exists())
        self.assertFalse(Testimonial.objects.exists())
        self.assertEqual(ServiceCategory.objects.count(), 6)  # haqiqiy kontent qoladi

    def test_demo_data_refuses_in_production(self):
        from django.core.management import CommandError

        with self.settings(DEBUG=False), self.assertRaises(CommandError):
            self.call("demo_data")

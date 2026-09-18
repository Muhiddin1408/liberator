from django.contrib.auth.models import User
from django.core.cache import cache
from django.core.validators import RegexValidator
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import get_language
from django_ckeditor_5.fields import CKEditor5Field

from app.utils import OptimizedImagesMixin, unique_slug, validate_image_size

LANG_SUFFIXES = ("ru", "en")


class LocalizedMixin:
    """Aktiv tilga mos maydon qiymatini qaytaradi.

    Asosiy (UZ) qiymat `<field>` da, tarjimalar `<field>_ru` / `<field>_en` da.
    Tarjima bo'sh bo'lsa UZ qiymatiga qaytadi. Shablonda: `{{ obj|tr:"name" }}`.
    """

    def tr(self, field):
        lang = (get_language() or "uz")[:2]
        if lang in LANG_SUFFIXES:
            value = getattr(self, f"{field}_{lang}", None)
            if value:
                return value
        return getattr(self, field) or ""


# --- Sayt sozlamalari --------------------------------------------------------

class SiteSettings(LocalizedMixin, models.Model):
    """Kontaktlar, manzil va ijtimoiy tarmoqlar — yagona yozuv, admin'dan tahrirlanadi."""

    CACHE_KEY = "site_settings"

    phone_primary = models.CharField("Asosiy telefon", max_length=32, default="+998555122992")
    phone_secondary = models.CharField("Qo'shimcha telefon", max_length=32, blank=True, default="+998998088889")
    email = models.EmailField("Email", default="Liberator.inbox@gmail.com")

    address = models.CharField(
        "Manzil", max_length=255,
        default="Toshkent shahri, Yashnobod tumani, Sodiq Azimov ko‘chasi 68-uy",
    )
    address_ru = models.CharField(
        "Manzil (RU)", max_length=255, blank=True,
        default="г. Ташкент, Яшнабадский район, ул. Садыка Азимова, 68",
    )
    address_en = models.CharField(
        "Manzil (EN)", max_length=255, blank=True,
        default="68 Sodiq Azimov Street, Yashnobod District, Tashkent",
    )
    working_hours = models.CharField("Ish vaqti", max_length=120, default="Dushanba–Shanba: 09:00 – 18:00")
    working_hours_ru = models.CharField("Ish vaqti (RU)", max_length=120, blank=True,
                                        default="Понедельник–Суббота: 09:00 – 18:00")
    working_hours_en = models.CharField("Ish vaqti (EN)", max_length=120, blank=True,
                                        default="Mon–Sat: 09:00 – 18:00")

    latitude = models.DecimalField("Kenglik", max_digits=9, decimal_places=6, default=41.303795)
    longitude = models.DecimalField("Uzunlik", max_digits=9, decimal_places=6, default=69.288944)

    telegram_url = models.URLField("Telegram", blank=True, help_text="Masalan: https://t.me/liberator_uz")
    whatsapp_phone = models.CharField("WhatsApp raqami", max_length=32, blank=True,
                                      help_text="Faqat raqamlar, masalan: 998998088889")
    instagram_url = models.URLField("Instagram", blank=True)
    facebook_url = models.URLField("Facebook", blank=True)
    youtube_url = models.URLField("YouTube", blank=True)
    linkedin_url = models.URLField("LinkedIn", blank=True)

    founded_year = models.PositiveIntegerField("Asos solingan yil", default=2010)
    meta_description = models.CharField(
        "SEO tavsif", max_length=160, blank=True,
        default="Liberator advokatlik firmasi — korporativ, fuqarolik, iqtisodiy va jinoyat ishlari "
                "bo‘yicha malakali yuridik yordam. Bepul konsultatsiya.",
        help_text="Google natijalarida ko'rinadigan 150–160 belgilik tavsif.",
    )
    meta_description_ru = models.CharField("SEO tavsif (RU)", max_length=160, blank=True,
                                           default="Адвокатская фирма Liberator — корпоративное, гражданское, "
                                                   "экономическое и уголовное право в Ташкенте. "
                                                   "Бесплатная консультация.")
    meta_description_en = models.CharField("SEO tavsif (EN)", max_length=160, blank=True,
                                           default="Liberator law firm in Tashkent — corporate, civil, "
                                                   "commercial and criminal law. Free initial consultation.")

    class Meta:
        verbose_name = "Sayt sozlamalari"
        verbose_name_plural = "Sayt sozlamalari"

    def __str__(self):
        return "Sayt sozlamalari"

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)
        cache.delete(self.CACHE_KEY)

    def delete(self, *args, **kwargs):
        pass

    @classmethod
    def load(cls):
        obj = cache.get(cls.CACHE_KEY)
        if obj is None:
            obj, _ = cls.objects.get_or_create(pk=1)
            cache.set(cls.CACHE_KEY, obj, 60 * 15)
        return obj

    @property
    def whatsapp_url(self):
        digits = "".join(ch for ch in self.whatsapp_phone if ch.isdigit())
        return f"https://wa.me/{digits}" if digits else ""

    @property
    def map_embed_url(self):
        return (f"https://yandex.uz/map-widget/v1/?ll={self.longitude}%2C{self.latitude}"
                f"&z=17&l=map&pt={self.longitude},{self.latitude},pm2rdl")

    @property
    def map_link(self):
        return f"https://yandex.uz/maps/?pt={self.longitude},{self.latitude}&z=17&l=map"

    @property
    def phones(self):
        return [p for p in (self.phone_primary, self.phone_secondary) if p]


# --- Jamoa -------------------------------------------------------------------

class Staff(OptimizedImagesMixin, LocalizedMixin, models.Model):
    image_fields = {"image": 900}

    # --- O'zbekcha (asosiy til) ---
    full_name = models.CharField("F.I.O", max_length=200)
    position = models.CharField("Lavozim", max_length=200)
    short_description = models.CharField(
        "Qisqa tavsif", max_length=300, blank=True,
        help_text="Card ostida ko'rinadigan 1-2 qatorlik qisqa matn.",
    )
    specialization = CKEditor5Field("Mutaxassislik", blank=True)
    practice = CKEditor5Field("Amaliyot", blank=True)

    # --- Русский ---
    full_name_ru = models.CharField("F.I.O (RU)", max_length=200, blank=True)
    position_ru = models.CharField("Lavozim (RU)", max_length=200, blank=True)
    short_description_ru = models.CharField("Qisqa tavsif (RU)", max_length=300, blank=True)
    specialization_ru = CKEditor5Field("Mutaxassislik (RU)", blank=True)
    practice_ru = CKEditor5Field("Amaliyot (RU)", blank=True)

    # --- English ---
    full_name_en = models.CharField("F.I.O (EN)", max_length=200, blank=True)
    position_en = models.CharField("Lavozim (EN)", max_length=200, blank=True)
    short_description_en = models.CharField("Qisqa tavsif (EN)", max_length=300, blank=True)
    specialization_en = CKEditor5Field("Mutaxassislik (EN)", blank=True)
    practice_en = CKEditor5Field("Amaliyot (EN)", blank=True)

    image = models.ImageField(
        "Rasm", upload_to="staff/%Y/%m/", blank=True, null=True,
        validators=[validate_image_size],
        help_text="Tavsiya: 600x700px. Yuklangan rasm avtomatik siqiladi (WebP).",
    )

    phone = models.CharField("Telefon", max_length=32, blank=True)
    email = models.EmailField("Email", blank=True)
    telegram = models.URLField("Telegram", blank=True)
    linkedin = models.URLField("LinkedIn", blank=True)

    slug = models.SlugField("Slug", max_length=220, unique=True, blank=True)
    order = models.PositiveIntegerField("Tartib", default=0, db_index=True)
    is_active = models.BooleanField("Faol", default=True, db_index=True)

    created_at = models.DateTimeField("Yaratilgan", auto_now_add=True)
    updated_at = models.DateTimeField("Yangilangan", auto_now=True)

    class Meta:
        verbose_name = "Jamoa a'zosi"
        verbose_name_plural = "Jamoa"
        ordering = ("order", "id")
        indexes = [
            models.Index(fields=("is_active", "order")),
        ]

    def __str__(self):
        return self.full_name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slug(self, self.full_name, fallback="staff")
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("team_detail", kwargs={"slug": self.slug})

    @property
    def localized_full_name(self):
        return self.tr("full_name")

    @property
    def localized_position(self):
        return self.tr("position")

    @property
    def localized_short_description(self):
        return self.tr("short_description")

    @property
    def localized_specialization(self):
        return self.tr("specialization")

    @property
    def localized_practice(self):
        return self.tr("practice")

    @property
    def image_url(self):
        if self.image and hasattr(self.image, "url"):
            try:
                return self.image.url
            except ValueError:
                pass
        return None


# --- Xizmatlar -----------------------------------------------------------------

class ActiveQuerySet(models.QuerySet):
    def active(self):
        return self.filter(is_active=True)


class ServiceCategory(OptimizedImagesMixin, LocalizedMixin, models.Model):
    image_fields = {"image": 1600}

    name = models.CharField("Nomi", max_length=100, unique=True)
    name_ru = models.CharField("Nomi (RU)", max_length=100, unique=True, blank=True, null=True)
    name_en = models.CharField("Nomi (EN)", max_length=100, unique=True, blank=True, null=True)
    description = models.TextField("Tavsif", blank=True, null=True)
    description_ru = models.TextField("Tavsif (RU)", blank=True, null=True)
    description_en = models.TextField("Tavsif (EN)", blank=True, null=True)
    image = models.ImageField("Rasm", upload_to="service_categories/%Y/%m/%d", blank=True, null=True,
                              validators=[validate_image_size])
    slug = models.SlugField("Slug", max_length=120, unique=True, blank=True,
                            help_text="URL uchun: /uz/xizmatlar/<slug>/. Bo'sh qoldirilsa nomdan yasaladi.")
    order = models.PositiveIntegerField("Tartib", default=0, db_index=True)
    is_active = models.BooleanField("Faol", default=True)

    objects = ActiveQuerySet.as_manager()

    class Meta:
        verbose_name = "Xizmat yo'nalishi"
        verbose_name_plural = "Xizmat yo'nalishlari"
        ordering = ("order", "id")

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slug(self, self.name, fallback="xizmat", max_length=120)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("service_category", kwargs={"slug": self.slug})


class Service(LocalizedMixin, models.Model):
    category = models.ForeignKey(ServiceCategory, on_delete=models.CASCADE, related_name="services",
                                 verbose_name="Yo'nalish")
    title = models.CharField("Nomi", max_length=200)
    title_ru = models.CharField("Nomi (RU)", max_length=200, blank=True, null=True)
    title_en = models.CharField("Nomi (EN)", max_length=200, blank=True, null=True)
    description = models.TextField("Tavsif", blank=True, null=True)
    description_ru = models.TextField("Tavsif (RU)", blank=True, null=True)
    description_en = models.TextField("Tavsif (EN)", blank=True, null=True)
    slug = models.SlugField("Slug", max_length=220, unique=True, blank=True)
    order = models.PositiveIntegerField("Tartib", default=0, db_index=True)
    is_active = models.BooleanField("Faol", default=True)

    objects = ActiveQuerySet.as_manager()

    class Meta:
        verbose_name = "Xizmat"
        verbose_name_plural = "Xizmatlar"
        ordering = ("order", "id")

    def __str__(self):
        return f"{self.title} ({self.category.name})"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slug(self, self.title, fallback="xizmat", max_length=220)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("service_detail", kwargs={"category_slug": self.category.slug, "slug": self.slug})


# --- Murojaatlar (lead) --------------------------------------------------------

phone_validator = RegexValidator(
    regex=r"^\+?[\d\s\-()]{9,20}$",
    message="Telefon raqamini to'g'ri kiriting, masalan: +998 90 123 45 67",
)


class ConsultationRequest(models.Model):
    KIND_CONSULTATION = "consultation"
    KIND_CALLBACK = "callback"
    KIND_CHOICES = (
        (KIND_CONSULTATION, "Konsultatsiya"),
        (KIND_CALLBACK, "Qayta qo'ng'iroq"),
    )

    STATUS_NEW = "new"
    STATUS_CHOICES = (
        (STATUS_NEW, "Yangi"),
        ("contacted", "Bog'lanildi"),
        ("in_progress", "Jarayonda"),
        ("closed", "Yopildi"),
        ("spam", "Spam"),
    )

    kind = models.CharField("Turi", max_length=20, choices=KIND_CHOICES, default=KIND_CONSULTATION)
    full_name = models.CharField("Ism", max_length=150)
    phone = models.CharField("Telefon", max_length=20, validators=[phone_validator])
    email = models.EmailField("Email", blank=True)
    service = models.ForeignKey(ServiceCategory, null=True, blank=True, on_delete=models.SET_NULL,
                                related_name="requests", verbose_name="Yo'nalish")
    staff = models.ForeignKey(Staff, null=True, blank=True, on_delete=models.SET_NULL,
                              related_name="requests", verbose_name="Advokat")
    message = models.TextField("Xabar", blank=True)
    source_page = models.CharField("Qaysi sahifadan", max_length=255, blank=True)
    language = models.CharField("Til", max_length=5, blank=True)
    status = models.CharField("Holat", max_length=20, choices=STATUS_CHOICES, default=STATUS_NEW, db_index=True)
    admin_note = models.TextField("Admin izohi", blank=True)
    ip_address = models.GenericIPAddressField("IP manzil", null=True, blank=True)
    created_at = models.DateTimeField("Yuborilgan", auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField("Yangilangan", auto_now=True)

    class Meta:
        verbose_name = "Murojaat"
        verbose_name_plural = "Murojaatlar"
        ordering = ("-created_at",)

    def __str__(self):
        return f"{self.full_name} — {self.phone} ({self.created_at:%d.%m.%Y %H:%M})"


# --- Kontent -----------------------------------------------------------------------

class PublishedQuerySet(models.QuerySet):
    def published(self):
        return self.filter(is_published=True, published_at__lte=timezone.now())


class News(OptimizedImagesMixin, LocalizedMixin, models.Model):
    image_fields = {"image": 1600}

    title = models.CharField("Sarlavha", max_length=220)
    title_ru = models.CharField("Sarlavha (RU)", max_length=220, blank=True)
    title_en = models.CharField("Sarlavha (EN)", max_length=220, blank=True)
    summary = models.CharField("Qisqa mazmun", max_length=300, blank=True,
                               help_text="Ro'yxatda va Google'da ko'rinadi (150–160 belgi ideal).")
    summary_ru = models.CharField("Qisqa mazmun (RU)", max_length=300, blank=True)
    summary_en = models.CharField("Qisqa mazmun (EN)", max_length=300, blank=True)
    body = CKEditor5Field("Matn")
    body_ru = CKEditor5Field("Matn (RU)", blank=True)
    body_en = CKEditor5Field("Matn (EN)", blank=True)
    image = models.ImageField("Rasm", upload_to="news/%Y/%m/", blank=True, null=True,
                              validators=[validate_image_size])
    author = models.ForeignKey(Staff, null=True, blank=True, on_delete=models.SET_NULL,
                               related_name="articles", verbose_name="Muallif")
    slug = models.SlugField("Slug", max_length=240, unique=True, blank=True)
    is_published = models.BooleanField("E'lon qilingan", default=False, db_index=True)
    published_at = models.DateTimeField("E'lon qilingan sana", default=timezone.now, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = PublishedQuerySet.as_manager()

    class Meta:
        verbose_name = "Maqola"
        verbose_name_plural = "Yangiliklar va maqolalar"
        ordering = ("-published_at",)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slug(self, self.title, fallback="maqola", max_length=240)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("news_detail", kwargs={"slug": self.slug})


class Testimonial(OptimizedImagesMixin, LocalizedMixin, models.Model):
    """Faqat haqiqiy mijozlardan, ularning yozma roziligi bilan."""

    image_fields = {"photo": 400}

    author_name = models.CharField("Mijoz ismi", max_length=150)
    author_position = models.CharField("Lavozimi / kompaniya", max_length=150, blank=True)
    author_position_ru = models.CharField("Lavozimi (RU)", max_length=150, blank=True)
    author_position_en = models.CharField("Lavozimi (EN)", max_length=150, blank=True)
    text = models.TextField("Sharh")
    text_ru = models.TextField("Sharh (RU)", blank=True)
    text_en = models.TextField("Sharh (EN)", blank=True)
    photo = models.ImageField("Rasm", upload_to="testimonials/", blank=True, null=True,
                              validators=[validate_image_size])
    consent_received = models.BooleanField(
        "Mijoz roziligi olingan", default=False,
        help_text="Sharh faqat mijozning yozma roziligi bilan e'lon qilinadi.",
    )
    is_published = models.BooleanField("E'lon qilingan", default=False)
    order = models.PositiveIntegerField("Tartib", default=0)

    class Meta:
        verbose_name = "Mijoz sharhi"
        verbose_name_plural = "Mijozlar sharhlari"
        ordering = ("order", "-id")

    def __str__(self):
        return self.author_name


class Achievement(LocalizedMixin, models.Model):
    """Bosh sahifadagi raqamlar. Faqat tekshirilgan, haqiqiy ko'rsatkichlar kiritilsin."""

    value = models.CharField("Qiymat", max_length=20, help_text="Masalan: 1200+ yoki 15")
    label = models.CharField("Izoh", max_length=100, help_text="Masalan: yutilgan ish")
    label_ru = models.CharField("Izoh (RU)", max_length=100, blank=True)
    label_en = models.CharField("Izoh (EN)", max_length=100, blank=True)
    order = models.PositiveIntegerField("Tartib", default=0)
    is_active = models.BooleanField("Faol", default=True)

    objects = ActiveQuerySet.as_manager()

    class Meta:
        verbose_name = "Ko'rsatkich"
        verbose_name_plural = "Ko'rsatkichlar (raqamlar)"
        ordering = ("order", "id")

    def __str__(self):
        return f"{self.value} {self.label}"


class FAQ(LocalizedMixin, models.Model):
    question = models.CharField("Savol", max_length=255)
    question_ru = models.CharField("Savol (RU)", max_length=255, blank=True)
    question_en = models.CharField("Savol (EN)", max_length=255, blank=True)
    answer = models.TextField("Javob")
    answer_ru = models.TextField("Javob (RU)", blank=True)
    answer_en = models.TextField("Javob (EN)", blank=True)
    category = models.ForeignKey(ServiceCategory, null=True, blank=True, on_delete=models.SET_NULL,
                                 related_name="faqs", verbose_name="Yo'nalish",
                                 help_text="Bo'sh bo'lsa — umumiy savol (aloqa sahifasida chiqadi).")
    order = models.PositiveIntegerField("Tartib", default=0)
    is_active = models.BooleanField("Faol", default=True)

    objects = ActiveQuerySet.as_manager()

    class Meta:
        verbose_name = "Savol-javob"
        verbose_name_plural = "Ko'p beriladigan savollar"
        ordering = ("order", "id")

    def __str__(self):
        return self.question


class LegalPage(LocalizedMixin, models.Model):
    """Maxfiylik siyosati, foydalanish shartlari va shu kabi sahifalar."""

    PRIVACY = "privacy"
    TERMS = "terms"
    KIND_CHOICES = ((PRIVACY, "Maxfiylik siyosati"), (TERMS, "Foydalanish shartlari"))

    kind = models.CharField("Sahifa", max_length=20, choices=KIND_CHOICES, unique=True)
    title = models.CharField("Sarlavha", max_length=200)
    title_ru = models.CharField("Sarlavha (RU)", max_length=200, blank=True)
    title_en = models.CharField("Sarlavha (EN)", max_length=200, blank=True)
    body = CKEditor5Field("Matn")
    body_ru = CKEditor5Field("Matn (RU)", blank=True)
    body_en = CKEditor5Field("Matn (EN)", blank=True)
    updated_at = models.DateTimeField("Yangilangan", auto_now=True)

    class Meta:
        verbose_name = "Huquqiy sahifa"
        verbose_name_plural = "Huquqiy sahifalar"

    def __str__(self):
        return self.get_kind_display()


# --- Hamkorlar va ichki statistika ----------------------------------------------------

class CaseStatistic(models.Model):
    """Ichki hisob uchun (saytda ko'rsatilmaydi — mijoz ismlari maxfiy)."""

    CASE_TYPE_CHOICES = (
        ("criminal", "Jinoyat ishi"),
        ("civil", "Fuqarolik ishi"),
        ("administrative", "Ma'muriy ish"),
        ("economic", "Iqtisodiy ish"),
    )

    case_type = models.CharField("Ish turi", max_length=20, choices=CASE_TYPE_CHOICES)
    staff = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="cases",
                              verbose_name="Mas'ul")
    service = models.ForeignKey("Service", on_delete=models.SET_NULL, null=True, blank=True, related_name="cases",
                                verbose_name="Xizmat")
    client_name = models.CharField("Mijoz", max_length=200)
    opened_at = models.DateField("Ochilgan", auto_now_add=True)
    closed_at = models.DateField("Yopilgan", blank=True, null=True)
    status = models.CharField("Holat", max_length=50, default="open")
    notes = models.TextField("Izoh", blank=True, null=True)

    class Meta:
        verbose_name = "Ish (ichki hisob)"
        verbose_name_plural = "Ishlar (ichki hisob)"

    def __str__(self):
        return f"{self.client_name} -  ({self.status})"


class Partner(OptimizedImagesMixin, models.Model):
    image_fields = {"icon": 400}

    name = models.CharField("Nomi", max_length=200)
    partner_type = models.CharField(
        "Turi",
        max_length=50,
        choices=(
            ("lawyer", "Advokat"),
            ("company", "Kompaniya"),
            ("organization", "Tashkilot"),
            ("other", "Boshqa"),
        ),
        default="other",
    )
    phone_number = models.CharField("Telefon", max_length=20, blank=True, null=True)
    email = models.EmailField("Email", blank=True, null=True)
    address = models.CharField("Manzil", max_length=255, blank=True, null=True)
    website = models.URLField("Veb-sayt", blank=True, null=True)

    icon = models.ImageField(
        "Logotip", upload_to="partners/icons/", blank=True, null=True,
        validators=[validate_image_size],
        help_text="Hamkor logotipi (faqat ularning roziligi bilan).",
    )

    notes = models.TextField("Izoh", blank=True, null=True)
    is_active = models.BooleanField("Faol", default=True)
    order = models.PositiveIntegerField("Tartib", default=0)
    joined_at = models.DateField(auto_now_add=True)

    objects = ActiveQuerySet.as_manager()

    class Meta:
        verbose_name = "Hamkor"
        verbose_name_plural = "Hamkorlar"
        ordering = ("order", "id")

    def __str__(self):
        return f"{self.name} ({self.get_partner_type_display()})"

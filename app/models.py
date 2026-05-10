from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify

try:
    from ckeditor.fields import RichTextField
except ImportError:
    RichTextField = models.TextField


class Staff(models.Model):
    full_name = models.CharField("F.I.O", max_length=200)
    position = models.CharField("Lavozim", max_length=200)
    short_description = models.CharField(
        "Qisqa tavsif",
        max_length=300,
        blank=True,
        help_text="Card ostida ko'rinadigan 1-2 qatorlik qisqa matn.",
    )
    specialization = RichTextField("Mutaxassislik", blank=True)
    practice = RichTextField("Amaliyot", blank=True)

    image = models.ImageField(
        "Rasm",
        upload_to="staff/%Y/%m/",
        blank=True,
        null=True,
        help_text="Tavsiya: 600x700px, kvadratga yaqin format.",
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
            base = slugify(self.full_name, allow_unicode=False) or "staff"
            slug = base
            i = 2
            qs = Staff.objects.exclude(pk=self.pk)
            while qs.filter(slug=slug).exists():
                slug = f"{base}-{i}"
                i += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("team_detail", kwargs={"slug": self.slug})

    @property
    def image_url(self):
        if self.image and hasattr(self.image, "url"):
            try:
                return self.image.url
            except ValueError:
                pass
        return None


class ServiceCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    name_ru = models.CharField(max_length=100, unique=True, blank=True, null=True)
    name_en = models.CharField(max_length=100, unique=True, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    description_ru = models.CharField(max_length=100, blank=True, null=True)
    description_en = models.CharField(max_length=100, blank=True, null=True)
    image = models.ImageField(upload_to="service_categories/%Y/%m/%d", blank=True, null=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Service Category"
        verbose_name_plural = "Service Categories"

    def __str__(self):
        return self.name


class Service(models.Model):
    category = models.ForeignKey(ServiceCategory, on_delete=models.CASCADE, related_name="services")
    title = models.CharField(max_length=200)
    title_ru = models.CharField(max_length=100, blank=True, null=True)
    title_en = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    description_ru = models.TextField(blank=True, null=True)
    description_en = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Service"
        verbose_name_plural = "Services"

    def __str__(self):
        return f"{self.title} ({self.category.name})"


class CaseStatistic(models.Model):
    CASE_TYPE_CHOICES = (
        ("criminal", "Criminal Case"),
        ("civil", "Civil Case"),
        ("administrative", "Administrative Case"),
        ("economic", "Economic Case"),
    )

    case_type = models.CharField(max_length=20, choices=CASE_TYPE_CHOICES)
    staff = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="cases")
    service = models.ForeignKey("Service", on_delete=models.SET_NULL, null=True, blank=True, related_name="cases")
    client_name = models.CharField(max_length=200)
    opened_at = models.DateField(auto_now_add=True)
    closed_at = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=50, default="open")
    notes = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Case Statistic"
        verbose_name_plural = "Case Statistics"

    def __str__(self):
        return f"{self.client_name} -  ({self.status})"


class Partner(models.Model):
    name = models.CharField(max_length=200)
    partner_type = models.CharField(
        max_length=50,
        choices=(
            ("lawyer", "Lawyer"),
            ("company", "Company"),
            ("organization", "Organization"),
            ("other", "Other"),
        ),
        default="other",
    )
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    website = models.URLField(blank=True, null=True)

    icon = models.ImageField(
        upload_to="partners/icons/", blank=True, null=True,
        help_text="Upload partner logo or icon"
    )

    notes = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    joined_at = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = "Partner"
        verbose_name_plural = "Partners"

    def __str__(self):
        return f"{self.name} ({self.get_partner_type_display()})"

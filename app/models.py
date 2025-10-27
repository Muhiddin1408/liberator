from django.db import models
from django.contrib.auth.models import User


class Staff(models.Model):
    ROLE_CHOICES = (
        ("lawyer", "Lawyer"),
        ("assistant", "Assistant"),
        ("secretary", "Secretary"),
        ("accountant", "Accountant"),
        ("admin", "Administrator"),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="staff")
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    hire_date = models.DateField(auto_now_add=True)
    specialization = models.CharField(max_length=100, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    notes = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to="staff/%Y/%m/%d", blank=True, null=True)

    def __str__(self):
        return f"{self.user} "


class ServiceCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Service Category"
        verbose_name_plural = "Service Categories"

    def __str__(self):
        return self.name


class Service(models.Model):
    category = models.ForeignKey(ServiceCategory, on_delete=models.CASCADE, related_name="services")
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Service"
        verbose_name_plural = "Services"

    def __str__(self):
        return f"{self.title} ({self.category.name})"

from django.db import models
from django.contrib.auth.models import User


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
    client_name = models.CharField(max_length=200)              # mijoz kim
    opened_at = models.DateField(auto_now_add=True)             # ish ochilgan sana
    closed_at = models.DateField(blank=True, null=True)         # yopilgan sana (agar yopilgan bo‘lsa)
    status = models.CharField(max_length=50, default="open")    # open / closed / pending
    notes = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Case Statistic"
        verbose_name_plural = "Case Statistics"

    def __str__(self):
        return f"{self.client_name} -  ({self.status})"


class Partner(models.Model):
    name = models.CharField(max_length=200)  # Hamkor nomi
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

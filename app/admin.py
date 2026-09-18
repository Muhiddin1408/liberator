from django.contrib import admin
from django.utils.html import format_html
from django.utils.text import Truncator

from app.models import (
    FAQ, Achievement, CaseStatistic, ConsultationRequest, LegalPage, News, Partner, Service, ServiceCategory,
    SiteSettings, Staff, Testimonial,
)


def image_thumb(url, size=48, round_=True):
    radius = "50%" if round_ else "6px"
    return format_html(
        '<img src="{}" style="width:{}px;height:{}px;border-radius:{};object-fit:cover;border:1px solid #ddd;" />',
        url, size, size, radius,
    )


# --- Murojaatlar -------------------------------------------------------------------

@admin.register(ConsultationRequest)
class ConsultationRequestAdmin(admin.ModelAdmin):
    list_display = ("created_at", "full_name", "phone_link", "kind", "service", "staff", "status", "language")
    list_display_links = ("created_at", "full_name")
    list_editable = ("status",)
    list_filter = ("status", "kind", "service", "language", "created_at")
    search_fields = ("full_name", "phone", "email", "message")
    date_hierarchy = "created_at"
    readonly_fields = ("kind", "full_name", "phone", "email", "service", "staff", "message",
                       "source_page", "language", "ip_address", "created_at", "updated_at")
    fieldsets = (
        ("Murojaat", {"fields": ("kind", "full_name", "phone", "email", "service", "staff", "message")}),
        ("Ishlov berish", {"fields": ("status", "admin_note")}),
        ("Texnik", {"classes": ("collapse",),
                    "fields": ("source_page", "language", "ip_address", "created_at", "updated_at")}),
    )
    actions = ("mark_contacted", "mark_spam")

    def has_add_permission(self, request):
        return False

    @admin.display(description="Telefon", ordering="phone")
    def phone_link(self, obj):
        return format_html('<a href="tel:{}">{}</a>', obj.phone, obj.phone)

    @admin.action(description="Bog'lanildi deb belgilash")
    def mark_contacted(self, request, queryset):
        self.message_user(request, f"{queryset.update(status='contacted')} ta murojaat yangilandi.")

    @admin.action(description="Spam deb belgilash")
    def mark_spam(self, request, queryset):
        self.message_user(request, f"{queryset.update(status='spam')} ta murojaat spam deb belgilandi.")


# --- Sayt sozlamalari ------------------------------------------------------------------

@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    fieldsets = (
        ("Kontaktlar", {"fields": ("phone_primary", "phone_secondary", "email")}),
        ("Manzil va ish vaqti", {"fields": (
            "address", "address_ru", "address_en",
            "working_hours", "working_hours_ru", "working_hours_en",
            "latitude", "longitude",
        )}),
        ("Messenjer va ijtimoiy tarmoqlar", {"fields": (
            "telegram_url", "whatsapp_phone", "instagram_url", "facebook_url", "youtube_url", "linkedin_url",
        )}),
        ("SEO", {"fields": ("founded_year", "meta_description", "meta_description_ru", "meta_description_en")}),
    )

    def has_add_permission(self, request):
        return not SiteSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


# --- Jamoa ----------------------------------------------------------------------------

@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ("thumb", "full_name", "position", "order", "is_active", "created_at")
    list_display_links = ("thumb", "full_name")
    list_editable = ("order", "is_active")
    list_filter = ("is_active", "position")
    search_fields = (
        "full_name", "full_name_ru", "full_name_en",
        "position", "position_ru", "position_en",
        "specialization", "practice", "email", "phone",
    )
    prepopulated_fields = {"slug": ("full_name",)}
    readonly_fields = ("created_at", "updated_at", "image_preview")
    ordering = ("order", "id")
    list_per_page = 30
    save_on_top = True
    actions = ("make_active", "make_inactive")

    fieldsets = (
        ("O'zbekcha", {
            "fields": ("full_name", "position", "short_description", "specialization", "practice"),
        }),
        ("Русский", {
            "fields": ("full_name_ru", "position_ru", "short_description_ru", "specialization_ru", "practice_ru"),
        }),
        ("English", {
            "fields": ("full_name_en", "position_en", "short_description_en", "specialization_en", "practice_en"),
        }),
        ("Rasm va asosiy sozlamalar", {
            "fields": ("slug", "image", "image_preview", "order", "is_active"),
        }),
        ("Aloqa va ijtimoiy tarmoqlar", {
            "fields": ("phone", "email", "telegram", "linkedin"),
        }),
        ("Tizim", {
            "classes": ("collapse",),
            "fields": ("created_at", "updated_at"),
        }),
    )

    @admin.display(description="Rasm")
    def thumb(self, obj):
        if obj.image_url:
            return image_thumb(obj.image_url)
        return format_html(
            '<div style="width:48px;height:48px;border-radius:50%;background:#eee;'
            'display:flex;align-items:center;justify-content:center;color:#888;'
            'font-weight:600;">{}</div>',
            (obj.full_name[:1] or "?").upper(),
        )

    @admin.display(description="Rasmni ko'rib chiqish")
    def image_preview(self, obj):
        if obj.image_url:
            return format_html(
                '<img src="{}" style="max-width:240px;max-height:240px;'
                'border-radius:8px;border:1px solid #ddd;" />',
                obj.image_url,
            )
        return "Rasm yuklanmagan"

    @admin.display(description="Qisqa")
    def short_text(self, obj):
        return Truncator(obj.short_description).chars(60)

    @admin.action(description="Tanlanganlarni faollashtirish")
    def make_active(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f"{updated} ta xodim faollashtirildi.")

    @admin.action(description="Tanlanganlarni nofaol qilish")
    def make_inactive(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f"{updated} ta xodim nofaol qilindi.")


# --- Xizmatlar ---------------------------------------------------------------------------

class ServiceInline(admin.StackedInline):
    model = Service
    extra = 0
    fields = (("title", "title_ru", "title_en"), ("description", "description_ru", "description_en"),
              ("slug", "order", "is_active"))


class FAQInline(admin.StackedInline):
    model = FAQ
    extra = 0
    fields = (("question", "question_ru", "question_en"), ("answer", "answer_ru", "answer_en"),
              ("order", "is_active"))


@admin.register(ServiceCategory)
class ServiceCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "order", "is_active")
    list_editable = ("order", "is_active")
    search_fields = ("name", "name_ru", "name_en", "description")
    list_filter = ("is_active",)
    prepopulated_fields = {"slug": ("name",)}
    fieldsets = (
        (None, {"fields": ("name", "name_ru", "name_en", "slug", "image", "order", "is_active")}),
        ("Tavsif (300–500 so'z tavsiya etiladi — SEO uchun)", {
            "fields": ("description", "description_ru", "description_en"),
        }),
    )
    inlines = (ServiceInline, FAQInline)


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "order", "is_active")
    list_editable = ("order", "is_active")
    list_filter = ("is_active", "category")
    search_fields = ("title", "title_ru", "title_en", "description")
    prepopulated_fields = {"slug": ("title",)}


# --- Kontent -------------------------------------------------------------------------------

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "published_at", "is_published")
    list_editable = ("is_published",)
    list_filter = ("is_published", "author")
    search_fields = ("title", "title_ru", "title_en", "summary", "body")
    date_hierarchy = "published_at"
    prepopulated_fields = {"slug": ("title",)}
    autocomplete_fields = ("author",)
    fieldsets = (
        ("O'zbekcha", {"fields": ("title", "summary", "body")}),
        ("Русский", {"classes": ("collapse",), "fields": ("title_ru", "summary_ru", "body_ru")}),
        ("English", {"classes": ("collapse",), "fields": ("title_en", "summary_en", "body_en")}),
        ("Nashr", {"fields": ("slug", "image", "author", "is_published", "published_at")}),
    )



@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ("author_name", "author_position", "consent_received", "is_published", "order")
    list_editable = ("is_published", "order")
    list_filter = ("is_published", "consent_received")

    def save_model(self, request, obj, form, change):
        if obj.is_published and not obj.consent_received:
            obj.is_published = False
            self.message_user(request, "Mijoz roziligi belgilanmagan — sharh e'lon qilinmadi.", level="warning")
        super().save_model(request, obj, form, change)


@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    list_display = ("value", "label", "order", "is_active")
    list_editable = ("order", "is_active")


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ("question", "category", "order", "is_active")
    list_editable = ("order", "is_active")
    list_filter = ("category", "is_active")
    search_fields = ("question", "answer")


@admin.register(LegalPage)
class LegalPageAdmin(admin.ModelAdmin):
    list_display = ("kind", "title", "updated_at")


@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    list_display = ("logo", "name", "partner_type", "order", "is_active", "joined_at")
    list_display_links = ("logo", "name")
    list_editable = ("order", "is_active")
    list_filter = ("is_active", "partner_type")
    search_fields = ("name", "email", "phone_number")

    @admin.display(description="Logo")
    def logo(self, obj):
        return image_thumb(obj.icon.url, round_=False) if obj.icon else "—"


@admin.register(CaseStatistic)
class CaseStatisticAdmin(admin.ModelAdmin):
    list_display = ("client_name", "case_type", "status", "staff", "opened_at", "closed_at")
    list_filter = ("case_type", "status")
    search_fields = ("client_name", "notes")

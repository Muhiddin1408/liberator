from django.contrib import admin
from django.utils.html import format_html
from django.utils.text import Truncator

from app.models import ServiceCategory, Staff, Service, Partner

admin.site.site_header = "Liberator Administration"
admin.site.site_title = "Liberator Admin"
admin.site.index_title = "Boshqaruv paneli"


@admin.register(ServiceCategory)
class ServiceCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "is_active")
    search_fields = ("name", "name_ru", "name_en", "description")
    list_filter = ("is_active",)


@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = (
        "thumb",
        "full_name",
        "position",
        "order",
        "is_active",
        "created_at",
    )
    list_display_links = ("thumb", "full_name")
    list_editable = ("order", "is_active")
    list_filter = ("is_active", "position")
    search_fields = ("full_name", "position", "specialization", "practice", "email", "phone")
    prepopulated_fields = {"slug": ("full_name",)}
    readonly_fields = ("created_at", "updated_at", "image_preview")
    ordering = ("order", "id")
    list_per_page = 30
    save_on_top = True
    actions = ("make_active", "make_inactive")

    fieldsets = (
        ("Asosiy ma'lumotlar", {
            "fields": ("full_name", "position", "slug", "short_description", "image", "image_preview"),
        }),
        ("Professional ma'lumotlar", {
            "fields": ("specialization", "practice"),
        }),
        ("Aloqa va ijtimoiy tarmoqlar", {
            "fields": ("phone", "email", "telegram", "linkedin"),
        }),
        ("Ko'rsatish sozlamalari", {
            "fields": ("order", "is_active"),
        }),
        ("Tizim", {
            "classes": ("collapse",),
            "fields": ("created_at", "updated_at"),
        }),
    )

    @admin.display(description="Rasm")
    def thumb(self, obj):
        if obj.image_url:
            return format_html(
                '<img src="{}" style="width:48px;height:48px;border-radius:50%;'
                'object-fit:cover;border:1px solid #ddd;" />',
                obj.image_url,
            )
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


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "is_active")
    list_filter = ("is_active", "category")
    search_fields = ("title", "title_ru", "title_en", "description")


@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    list_display = ("name", "partner_type", "is_active", "joined_at")
    list_filter = ("is_active", "partner_type")
    search_fields = ("name", "email", "phone_number")

import json

from django import template
from django.utils.html import format_html
from django.utils.safestring import mark_safe

register = template.Library()

_JSON_ESCAPES = {ord(">"): "\\u003E", ord("<"): "\\u003C", ord("&"): "\\u0026"}


@register.filter
def tr(obj, field):
    """Aktiv tildagi qiymat: `{{ category|tr:"name" }}`."""
    if obj is None:
        return ""
    return obj.tr(field)


@register.simple_tag
def json_ld(*items):
    """Bir yoki bir nechta Schema.org obyektini <script type="application/ld+json"> sifatida chiqaradi."""
    blocks = []
    for data in items:
        if data:
            payload = json.dumps(data, ensure_ascii=False).translate(_JSON_ESCAPES)
            blocks.append(format_html('<script type="application/ld+json">{}</script>', mark_safe(payload)))
    return mark_safe("\n".join(blocks))


@register.simple_tag
def icon(name, css_class=""):
    """`{% icon "phone" %}` — includes/icons.html dagi SVG belgisini chiqaradi."""
    return format_html(
        '<svg class="i {}" aria-hidden="true" focusable="false"><use href="#i-{}"></use></svg>', css_class, name,
    )


@register.filter
def tel(phone):
    """`tel:` havolasi uchun faqat + va raqamlar."""
    return "".join(ch for ch in str(phone) if ch.isdigit() or ch == "+")


@register.filter
def phone_display(phone):
    """+998555122992 -> +998 (55) 512-29-92"""
    digits = "".join(ch for ch in str(phone) if ch.isdigit())
    if len(digits) == 12 and digits.startswith("998"):
        return f"+998 ({digits[3:5]}) {digits[5:8]}-{digits[8:10]}-{digits[10:]}"
    return phone

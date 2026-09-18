from io import BytesIO
from pathlib import Path

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.files.base import ContentFile
from django.utils.text import slugify
from PIL import Image, ImageOps


def unique_slug(instance, value, field="slug", fallback="item", max_length=200):
    """`value` dan slug yasaydi va shu model ichida takrorlanmasligini ta'minlaydi."""
    base = (slugify(value) or fallback)[: max_length - 5].strip("-") or fallback
    model = type(instance)
    qs = model._default_manager.exclude(pk=instance.pk)
    slug, i = base, 2
    while qs.filter(**{field: slug}).exists():
        slug = f"{base}-{i}"
        i += 1
    return slug


def validate_image_size(image):
    limit = settings.MAX_UPLOAD_IMAGE_MB
    if image and image.size > limit * 1024 * 1024:
        raise ValidationError(f"Rasm hajmi {limit} MB dan oshmasligi kerak.")


def compress_image(upload, max_px=1600, quality=82):
    """Yuklangan rasmni kichraytiradi va WebP formatiga o'giradi.

    Telefondan yuklangan 4-5 MB'lik rasm odatda 100-200 KB bo'lib qoladi.
    """
    img = Image.open(upload)
    img = ImageOps.exif_transpose(img)
    has_alpha = img.mode in ("RGBA", "LA") or (img.mode == "P" and "transparency" in img.info)
    img = img.convert("RGBA" if has_alpha else "RGB")
    img.thumbnail((max_px, max_px), Image.LANCZOS)
    buffer = BytesIO()
    img.save(buffer, "WEBP", quality=quality, method=6)
    return ContentFile(buffer.getvalue(), name=f"{Path(upload.name).stem}.webp")


class OptimizedImagesMixin:
    """Yangi yuklangan rasmlarni saqlashdan oldin siqadi.

    Modelda `image_fields = {"image": 1600}` ko'rinishida maydon va
    maksimal o'lcham (px) ko'rsatiladi.
    """

    image_fields = {}

    def save(self, *args, **kwargs):
        for name, max_px in self.image_fields.items():
            file = getattr(self, name)
            if file and not getattr(file, "_committed", True):
                try:
                    setattr(self, name, compress_image(file, max_px=max_px))
                except (OSError, ValueError):
                    # Pillow o'qiy olmagan fayl — ImageField validatsiyasi buni ushlaydi.
                    pass
        super().save(*args, **kwargs)


def client_ip(request):
    """Mijoz IP manzili. Proksi (nginx) orqasida NUM_PROXIES ni sozlang."""
    num_proxies = getattr(settings, "NUM_PROXIES", 0)
    if num_proxies:
        forwarded = [ip.strip() for ip in request.META.get("HTTP_X_FORWARDED_FOR", "").split(",") if ip.strip()]
        if len(forwarded) >= num_proxies:
            return forwarded[-num_proxies]
    return request.META.get("REMOTE_ADDR")

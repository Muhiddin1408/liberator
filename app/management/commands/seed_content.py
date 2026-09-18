"""Sayt kontentini (xizmatlar, savol-javoblar, maqolalar) uch tilda bazaga yuklaydi.

    python manage.py seed_content              # serverda: yangi yozuvlar YASHIRIN qo'shiladi
    python manage.py seed_content --publish    # darhol saytda ko'rinadi (lokal ko'rish uchun)
    python manage.py seed_content --overwrite  # mavjud matnlarni ham yangilaydi

Xavfsiz: mavjud yozuvlarda faqat BO'SH maydonlar to'ldiriladi (admin'da kiritilgan matn o'zgarmaydi).
Yangi yo'nalishlar nofaol, maqolalar e'lon qilinmagan holda qo'shiladi — firma yuristi ko'rib chiqib,
admin panelda yoqadi. Matnlar: app/content/*.py
"""
from django.core.management.base import BaseCommand
from django.db import transaction

from app.content.articles import ARTICLES
from app.content.faqs import FAQS
from app.content.practice_areas import PRACTICE_AREAS
from app.models import FAQ, News, Service, ServiceCategory

SUFFIXES = ("", "_ru", "_en")


def trilingual(field, values):
    return {f"{field}{suffix}": value for suffix, value in zip(SUFFIXES, values)}


class Command(BaseCommand):
    help = "Xizmatlar, savol-javoblar va maqolalarni uch tilda yuklaydi."

    def add_arguments(self, parser):
        parser.add_argument("--publish", action="store_true", help="Yangi yozuvlarni darhol saytda ko'rsatish")
        parser.add_argument("--overwrite", action="store_true", help="Mavjud matnlarni ham almashtirish")

    def handle(self, *args, **options):
        self.publish = options["publish"]
        self.overwrite = options["overwrite"]
        self.stats = {"created": 0, "updated": 0}
        with transaction.atomic():
            categories = self.load_practice_areas()
            self.load_faqs(categories)
            self.load_articles()
        self.stdout.write(self.style.SUCCESS(
            f"Tayyor: {self.stats['created']} ta yangi, {self.stats['updated']} ta to'ldirilgan yozuv."
        ))
        if not self.publish:
            self.stdout.write(
                "Yangi yo'nalishlar NOFAOL, maqolalar E'LON QILINMAGAN holda qo'shildi.\n"
                "Admin panelda matnlarni ko'rib chiqing va 'Faol' / 'E'lon qilingan' belgisini qo'ying."
            )

    def save(self, model, lookup, values, create_defaults):
        obj = model.objects.filter(**lookup).first()
        if obj is None:
            obj = model(**lookup, **values, **create_defaults)
            obj.save()
            self.stats["created"] += 1
            return obj
        changed = False
        for field, value in values.items():
            if self.overwrite or not getattr(obj, field):
                if getattr(obj, field) != value:
                    setattr(obj, field, value)
                    changed = True
        if changed:
            obj.save()
            self.stats["updated"] += 1
        return obj

    def load_practice_areas(self):
        categories = {}
        for order, area in enumerate(PRACTICE_AREAS):
            values = {**trilingual("name", area["name"]), **trilingual("description", area["description"])}
            category = self.save(ServiceCategory, {"slug": area["slug"]}, values,
                                 {"order": order, "is_active": self.publish})
            categories[area["slug"]] = category
            for s_order, service in enumerate(area["services"]):
                values = {
                    **trilingual("title", service["title"]),
                    **trilingual("description", service["description"]),
                }
                title = values.pop("title")
                self.save(Service, {"category": category, "title": title}, values,
                          {"order": s_order, "is_active": True})
        return categories

    def load_faqs(self, categories):
        for order, faq in enumerate(FAQS):
            values = {**trilingual("question", faq["question"]), **trilingual("answer", faq["answer"])}
            question = values.pop("question")
            self.save(FAQ, {"question": question}, values, {
                "category": categories.get(faq["category"]), "order": order, "is_active": self.publish,
            })

    def load_articles(self):
        for article in ARTICLES:
            values = {
                **trilingual("title", article["title"]),
                **trilingual("summary", article["summary"]),
                **trilingual("body", article["body"]),
            }
            self.save(News, {"slug": article["slug"]}, values, {"is_published": self.publish})

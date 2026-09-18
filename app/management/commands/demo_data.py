"""Lokal ishlab chiqish uchun namuna ma'lumotlar.

    python manage.py demo_data           # seed_content --publish + namuna jamoa va sharhlar
    python manage.py demo_data --clear   # faqat namuna jamoa va sharhlarni o'chiradi

Xizmatlar, savol-javoblar va maqolalar — haqiqiy kontent (app/content/, seed_content buyrug'i).
Advokatlar (rahbardan tashqari) va sharhlar esa O'YLAB TOPILGAN — jonli saytga qo'yish mumkin emas:
DEBUG=False bo'lsa buyruq ishlamaydi.
"""
from pathlib import Path

from django.conf import settings
from django.core.files import File
from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from app.models import News, Staff, Testimonial

PHOTO = Path(settings.BASE_DIR) / "static_file" / "site" / "img" / "director.jpg"

STAFF = [
    {
        "slug": "batirov-farrux-yusupovich",
        "full_name": ("Batirov Farrux Yusupovich", "Батиров Фаррух Юсупович", "Farrukh Batirov"),
        "position": ("Boshqaruvchi sherik", "Управляющий партнёр", "Managing partner"),
        "short": ("Firma asoschisi. Korporativ huquq va murakkab sud nizolari.",
                  "Основатель фирмы. Корпоративное право и сложные судебные споры.",
                  "Founder of the firm. Corporate law and complex litigation."),
        "specialization": "<p>Korporativ huquq, iqtisodiy va arbitraj nizolari, jinoyat ishlari bo‘yicha himoya.</p>",
        "practice": "<ul><li>Yirik korxonalarni yuridik hamrohlik qilish</li>"
                    "<li>Iqtisodiy sudlarda vakillik</li><li>Huquqiy audit (due diligence)</li></ul>",
        "photo": True,
    },
    {
        "slug": "demo-aziza-karimova",
        "full_name": ("Aziza Karimova", "Азиза Каримова", "Aziza Karimova"),
        "position": ("Advokat", "Адвокат", "Attorney"),
        "short": ("Fuqarolik va oilaviy nizolar.", "Гражданские и семейные споры.", "Civil and family disputes."),
        "specialization": "<p>Meros, oilaviy va shartnomaviy nizolar.</p>",
        "practice": "",
    },
    {
        "slug": "demo-jasur-rahimov",
        "full_name": ("Jasur Rahimov", "Жасур Рахимов", "Jasur Rakhimov"),
        "position": ("Advokat", "Адвокат", "Attorney"),
        "short": ("Jinoyat ishlari bo‘yicha himoya.", "Защита по уголовным делам.", "Criminal defence."),
        "specialization": "<p>Tergov va sud bosqichlarida himoya, iqtisodiy jinoyatlar.</p>",
        "practice": "",
    },
    {
        "slug": "demo-dilnoza-yusupova",
        "full_name": ("Dilnoza Yusupova", "Дилноза Юсупова", "Dilnoza Yusupova"),
        "position": ("Yurist", "Юрист", "Lawyer"),
        "short": ("Soliq va mehnat huquqi.", "Налоговое и трудовое право.", "Tax and employment law."),
        "specialization": "<p>Soliq tekshiruvlari, kadrlar hujjatlari auditi.</p>",
        "practice": "",
    },
]

TESTIMONIALS = [
    ("Namuna: S. Toshmatov", "Ishlab chiqarish korxonasi rahbari",
     "Korporativ nizoni sudgacha yetkazmasdan hal qilishdi. Har bir bosqichda nima bo‘layotganini tushuntirib borishdi."),
    ("Namuna: M. Aliyeva", "Xususiy mijoz",
     "Meros masalasida tez va aniq yordam berishdi. Hujjatlarni o‘zim yig‘ishim shart bo‘lmadi."),
    ("Namuna: D. Qodirov", "Logistika kompaniyasi direktori",
     "Soliq tekshiruvi davomida doimo yonimizda bo‘lishdi, natija kutganimizdan yaxshi chiqdi."),
]


class Command(BaseCommand):
    help = "Lokal ishlab chiqish uchun namuna ma'lumotlar qo'shadi (--clear bilan o'chiradi)."

    def add_arguments(self, parser):
        parser.add_argument("--clear", action="store_true", help="Namuna ma'lumotlarni o'chirish")
        parser.add_argument("--force", action="store_true", help="DEBUG=False bo'lsa ham ishga tushirish")

    def handle(self, *args, **options):
        if not settings.DEBUG and not options["force"]:
            raise CommandError("DEBUG=False: namuna ma'lumotlar jonli saytga qo'shilmaydi.")
        if options["clear"]:
            self.clear()
        else:
            self.load()

    @transaction.atomic
    def clear(self):
        Testimonial.objects.filter(author_name__in=[t[0] for t in TESTIMONIALS]).delete()
        # Slug VA ism mos kelsagina o'chiriladi — admin'da qo'lda kiritilgan haqiqiy yozuvlarga tegilmaydi.
        for data in STAFF:
            for staff in Staff.objects.filter(slug=data["slug"], full_name=data["full_name"][0]):
                if staff.image:
                    staff.image.delete(save=False)
                staff.delete()
        self.stdout.write(self.style.SUCCESS("Namuna jamoa va sharhlar o'chirildi."))

    def load(self):
        call_command("seed_content", "--publish", stdout=self.stdout)
        with transaction.atomic():
            staff_by_slug = self.load_staff()
            self.load_testimonials()
            # Maqolalarga namuna mualliflarni biriktiramiz (faqat muallifi yo'qlariga).
            authors = [staff_by_slug[s["slug"]] for s in STAFF]
            for i, article in enumerate(News.objects.filter(author__isnull=True).order_by("id")):
                article.author = authors[i % len(authors)]
                article.save(update_fields=["author"])
        self.stdout.write(self.style.SUCCESS(
            f"Namuna: {len(STAFF)} jamoa a'zosi, {len(TESTIMONIALS)} sharh. O'chirish: python manage.py demo_data --clear"
        ))

    def load_staff(self):
        staff_by_slug = {}
        for order, data in enumerate(STAFF):
            (uz, ru, en), (p_uz, p_ru, p_en), (d_uz, d_ru, d_en) = data["full_name"], data["position"], data["short"]
            staff, _ = Staff.objects.update_or_create(slug=data["slug"], defaults={
                "full_name": uz, "full_name_ru": ru, "full_name_en": en,
                "position": p_uz, "position_ru": p_ru, "position_en": p_en,
                "short_description": d_uz, "short_description_ru": d_ru, "short_description_en": d_en,
                "specialization": data["specialization"], "practice": data["practice"],
                "order": order, "is_active": True,
            })
            if data.get("photo") and not staff.image and PHOTO.exists():
                with PHOTO.open("rb") as fh:
                    staff.image = File(fh, name=PHOTO.name)
                    staff.save()
            staff_by_slug[data["slug"]] = staff
        return staff_by_slug

    def load_testimonials(self):
        for order, (name, position, text) in enumerate(TESTIMONIALS):
            Testimonial.objects.update_or_create(author_name=name, defaults={
                "author_position": position, "text": text, "order": order,
                "consent_received": True, "is_published": True,
            })

"""Lokal ishlab chiqish uchun namuna ma'lumotlar.

    python manage.py demo_data           # namuna ma'lumotlarni qo'shadi (qayta ishga tushirsa takrorlanmaydi)
    python manage.py demo_data --clear   # faqat shu buyruq qo'shgan yozuvlarni o'chiradi

DIQQAT: advokatlar (rahbardan tashqari), sharhlar va maqolalar — O'YLAB TOPILGAN.
Jonli saytga qo'yish mumkin emas: DEBUG=False bo'lsa buyruq ishlamaydi.
"""
from pathlib import Path

from django.conf import settings
from django.core.files import File
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.utils import timezone

from app.models import FAQ, News, Service, ServiceCategory, Staff, Testimonial

PHOTO = Path(settings.BASE_DIR) / "static_file" / "site" / "img" / "director.jpg"

CATEGORIES = [
    {
        "slug": "korporativ-huquq",
        "name": ("Korporativ huquq", "Корпоративное право", "Corporate law"),
        "description": (
            "Kompaniyalarni ro‘yxatdan o‘tkazish, ustav hujjatlari, aksiyadorlar va ishtirokchilar o‘rtasidagi "
            "nizolar, qo‘shilish va sotib olish bitimlari. Biznesingizni tashkil etishdan to qayta tashkil "
            "etishgacha yuridik hamrohlik qilamiz.",
            "Регистрация компаний, учредительные документы, корпоративные споры между участниками и "
            "акционерами, сделки слияния и поглощения. Сопровождаем бизнес от создания до реорганизации.",
            "Company formation, constitutional documents, shareholder and partner disputes, mergers and "
            "acquisitions. We support your business from incorporation to restructuring.",
        ),
        "services": [
            ("MChJ va AJ ro‘yxatdan o‘tkazish", "Регистрация ООО и АО", "LLC and JSC registration",
             "Ta’sis hujjatlarini tayyorlash, davlat ro‘yxatidan o‘tkazish va bank hisobini ochishda yordam."),
            ("Korporativ nizolar", "Корпоративные споры", "Corporate disputes",
             "Ishtirokchilar o‘rtasidagi nizolar, ulushlarni qaytarish va boshqaruv organlari qarorlarini nizolashish."),
            ("Qo‘shilish va sotib olish (M&A)", "Слияния и поглощения (M&A)", "Mergers and acquisitions (M&A)",
             "Bitim tuzilmasini ishlab chiqish, huquqiy audit va shartnomalarni tayyorlash."),
        ],
    },
    {
        "slug": "jinoyat-ishlari",
        "name": ("Jinoyat ishlari", "Уголовные дела", "Criminal defence"),
        "description": (
            "Tergovning barcha bosqichlarida va sudda advokat himoyasi, jabrlanuvchi manfaatlarini ifodalash, "
            "iqtisodiy jinoyatlar bo‘yicha ishlar. Himoya birinchi so‘roqdan boshlanadi.",
            "Защита на всех стадиях следствия и в суде, представительство потерпевших, дела об экономических "
            "преступлениях. Защита начинается с первого допроса.",
            "Defence at every stage of investigation and trial, representation of victims, white-collar crime. "
            "Defence starts from the very first interview.",
        ),
        "services": [
            ("Tergov bosqichida himoya", "Защита на стадии следствия", "Defence during investigation",
             "So‘roqlarda ishtirok, tergov harakatlarining qonuniyligini nazorat qilish."),
            ("Sudda himoya", "Защита в суде", "Defence in court",
             "Birinchi instansiya, apellyatsiya va kassatsiya sudlarida himoya."),
            ("Iqtisodiy jinoyatlar", "Экономические преступления", "Economic crimes",
             "Soliq, bojxona va mansabga oid ishlar bo‘yicha himoya."),
        ],
    },
    {
        "slug": "fuqarolik-nizolari",
        "name": ("Fuqarolik nizolari", "Гражданские споры", "Civil disputes"),
        "description": (
            "Shartnomaviy, mulkiy, meros va oilaviy nizolar bo‘yicha sudda vakillik. Avval muzokara yo‘li bilan "
            "hal qilishga harakat qilamiz, kerak bo‘lsa — sudda to‘liq himoya.",
            "Представительство в суде по договорным, имущественным, наследственным и семейным спорам. "
            "Сначала пытаемся решить вопрос переговорами, при необходимости — полная защита в суде.",
            "Representation in contractual, property, inheritance and family disputes. We try negotiation "
            "first and provide full court representation when needed.",
        ),
        "services": [
            ("Shartnomaviy nizolar", "Договорные споры", "Contract disputes",
             "Qarzni undirish, shartnoma bajarilmaganligi uchun zararni qoplash."),
            ("Meros va oilaviy ishlar", "Наследственные и семейные дела", "Inheritance and family matters",
             "Merosni rasmiylashtirish, mol-mulkni bo‘lish, aliment va vasiylik masalalari."),
        ],
    },
    {
        "slug": "soliq-huquqi",
        "name": ("Soliq huquqi", "Налоговое право", "Tax law"),
        "description": (
            "Soliq tekshiruvlarida hamrohlik, soliq organlari qarorlari ustidan shikoyat, soliq rejalashtirish "
            "va xavflarni baholash.",
            "Сопровождение налоговых проверок, обжалование решений налоговых органов, налоговое планирование "
            "и оценка рисков.",
            "Support during tax audits, appeals against tax authority decisions, tax planning and risk assessment.",
        ),
        "services": [
            ("Soliq tekshiruvlari", "Налоговые проверки", "Tax audits",
             "Tekshiruvga tayyorgarlik va jarayonda ishtirok etish."),
            ("Soliq nizolari", "Налоговые споры", "Tax disputes",
             "Soliq organlari qarorlarini ma’muriy va sud tartibida nizolashish."),
        ],
    },
    {
        "slug": "mehnat-huquqi",
        "name": ("Mehnat huquqi", "Трудовое право", "Employment law"),
        "description": (
            "Ish beruvchilar uchun kadrlar hujjatlari va ichki tartib qoidalari, xodimlar uchun noqonuniy "
            "ishdan bo‘shatish va ish haqi bo‘yicha nizolar.",
            "Для работодателей — кадровая документация и внутренние правила, для работников — споры о "
            "незаконном увольнении и заработной плате.",
            "HR documents and internal policies for employers; unlawful dismissal and wage disputes for employees.",
        ),
        "services": [
            ("Ishga tiklash", "Восстановление на работе", "Reinstatement",
             "Noqonuniy ishdan bo‘shatish ustidan sudga murojaat va majburiy progul uchun haq undirish."),
            ("Kadrlar hujjatlari auditi", "Аудит кадровых документов", "HR compliance audit",
             "Mehnat shartnomalari va buyruqlarni qonunchilikka moslashtirish."),
        ],
    },
    {
        "slug": "xorijiy-investitsiyalar",
        "name": ("Xorijiy investitsiyalar", "Иностранные инвестиции", "Foreign investment"),
        "description": (
            "O‘zbekistonga kirib kelayotgan xorijiy kompaniyalar uchun biznes tuzilmasini tanlash, ro‘yxatdan "
            "o‘tkazish, litsenziyalar va imtiyozlar bo‘yicha maslahat.",
            "Для иностранных компаний, выходящих на рынок Узбекистана: выбор структуры бизнеса, регистрация, "
            "лицензии и льготы.",
            "For foreign companies entering Uzbekistan: choosing a business structure, registration, licences "
            "and incentives.",
        ),
        "services": [
            ("Xorijiy kapitalli korxona ochish", "Открытие предприятия с иностранным капиталом",
             "Setting up a foreign-owned company",
             "Tuzilmani tanlash, hujjatlarni tayyorlash va ro‘yxatdan o‘tkazish."),
        ],
    },
]

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

NEWS = [
    {
        "slug": "demo-mehnat-shartnomasi-bekor-qilinganda",
        "title": ("Ishdan noqonuniy bo‘shatilsangiz nima qilish kerak",
                  "Что делать при незаконном увольнении", "What to do if you are unlawfully dismissed"),
        "summary": ("Ishga tiklanish uchun muddatlar, kerakli hujjatlar va sudga murojaat tartibi.",
                    "Сроки восстановления, нужные документы и порядок обращения в суд.",
                    "Deadlines for reinstatement, documents you need and how to go to court."),
        "body": "<p>Ishdan bo‘shatish to‘g‘risidagi buyruq nusxasini albatta oling. Nizolashish muddatlari "
                "qisqa, shuning uchun kechiktirmasdan advokat bilan maslahatlashing.</p>"
                "<h2>Qanday hujjatlar kerak</h2><ul><li>Mehnat shartnomasi</li><li>Bo‘shatish buyrug‘i</li>"
                "<li>Ish haqi to‘g‘risidagi ma’lumotnoma</li></ul>",
        "author": "demo-dilnoza-yusupova",
        "days_ago": 3,
    },
    {
        "slug": "demo-mchj-royxatdan-otkazish",
        "title": ("MChJ ochish: 5 ta asosiy qadam", "Открытие ООО: 5 основных шагов", "Opening an LLC: 5 key steps"),
        "summary": ("Ta’sischilar, ustav kapitali va ro‘yxatdan o‘tish — qisqa qo‘llanma.",
                    "Учредители, уставный капитал и регистрация — краткое руководство.",
                    "Founders, charter capital and registration — a short guide."),
        "body": "<p>MChJ — kichik va o‘rta biznes uchun eng keng tarqalgan shakl. Ta’sis hujjatlarini to‘g‘ri "
                "tuzish kelajakdagi korporativ nizolarning oldini oladi.</p>",
        "author": "batirov-farrux-yusupovich",
        "days_ago": 12,
    },
    {
        "slug": "demo-soliq-tekshiruviga-tayyorgarlik",
        "title": ("Soliq tekshiruviga qanday tayyorlanish kerak", "Как подготовиться к налоговой проверке",
                  "How to prepare for a tax audit"),
        "summary": ("Tekshiruvchilar birinchi navbatda nimaga e’tibor beradi va huquqlaringiz qanday.",
                    "На что проверяющие смотрят в первую очередь и каковы ваши права.",
                    "What inspectors look at first and what your rights are."),
        "body": "<p>Tekshiruv to‘g‘risidagi buyruqni talab qiling va uning doirasini aniqlang. Hujjatlarni faqat "
                "yozma so‘rov asosida taqdim eting.</p>",
        "author": "demo-dilnoza-yusupova",
        "days_ago": 25,
    },
]

FAQS = [
    (None, "Birinchi konsultatsiya bepulmi?", "Первая консультация бесплатная?", "Is the first consultation free?",
     "Ha. Birinchi qisqa konsultatsiyada vaziyatingizni baholaymiz va keyingi qadamlarni tushuntiramiz."),
    (None, "Qancha tez javob berasiz?", "Как быстро вы отвечаете?", "How quickly do you respond?",
     "Ish vaqtida murojaatlarga odatda 15–30 daqiqa ichida qo‘ng‘iroq qilamiz."),
    (None, "Onlayn maslahat berasizmi?", "Консультируете онлайн?", "Do you consult online?",
     "Ha, Telegram, WhatsApp yoki video qo‘ng‘iroq orqali maslahat berish mumkin."),
    (None, "Ma’lumotlarim maxfiy qoladimi?", "Мои данные останутся конфиденциальными?", "Will my data stay confidential?",
     "Ha. Advokatlik siri qonun bilan himoyalangan va uchinchi shaxslarga oshkor qilinmaydi."),
    ("korporativ-huquq", "MChJ ochish qancha vaqt oladi?", "Сколько времени занимает открытие ООО?",
     "How long does it take to open an LLC?",
     "Hujjatlar tayyor bo‘lsa, davlat ro‘yxatidan o‘tish odatda bir necha ish kunida yakunlanadi."),
    ("jinoyat-ishlari", "Advokatni qachon jalb qilish kerak?", "Когда нужно привлекать адвоката?",
     "When should I hire a lawyer?",
     "Imkon qadar erta — birinchi so‘roqdan oldin. Bu himoya imkoniyatlarini sezilarli oshiradi."),
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
        News.objects.filter(slug__in=[n["slug"] for n in NEWS]).delete()
        Testimonial.objects.filter(author_name__in=[t[0] for t in TESTIMONIALS]).delete()
        FAQ.objects.filter(question__in=[f[1] for f in FAQS]).delete()
        # Slug VA nom mos kelsagina o'chiriladi — keyin admin'da qo'lda kiritilgan haqiqiy yozuvlarga tegilmaydi.
        for data in CATEGORIES:
            ServiceCategory.objects.filter(slug=data["slug"], name=data["name"][0]).delete()
        for data in STAFF:
            for staff in Staff.objects.filter(slug=data["slug"], full_name=data["full_name"][0]):
                if staff.image:
                    staff.image.delete(save=False)
                staff.delete()
        self.stdout.write(self.style.SUCCESS("Namuna ma'lumotlar o'chirildi."))

    @transaction.atomic
    def load(self):
        categories = {}
        for order, data in enumerate(CATEGORIES):
            uz, ru, en = data["name"]
            category, _ = ServiceCategory.objects.update_or_create(slug=data["slug"], defaults={
                "name": uz, "name_ru": ru, "name_en": en, "order": order, "is_active": True,
                "description": data["description"][0], "description_ru": data["description"][1],
                "description_en": data["description"][2],
            })
            categories[data["slug"]] = category
            for s_order, (s_uz, s_ru, s_en, s_desc) in enumerate(data["services"]):
                Service.objects.update_or_create(category=category, title=s_uz, defaults={
                    "title_ru": s_ru, "title_en": s_en, "description": s_desc, "order": s_order, "is_active": True,
                })

        staff_by_slug = {}
        for order, data in enumerate(STAFF):
            (uz, ru, en), (p_uz, p_ru, p_en), (d_uz, d_ru, d_en) = data["full_name"], data["position"], data["short"]
            staff, created = Staff.objects.update_or_create(slug=data["slug"], defaults={
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

        for data in NEWS:
            uz, ru, en = data["title"]
            s_uz, s_ru, s_en = data["summary"]
            News.objects.update_or_create(slug=data["slug"], defaults={
                "title": uz, "title_ru": ru, "title_en": en,
                "summary": s_uz, "summary_ru": s_ru, "summary_en": s_en,
                "body": data["body"], "author": staff_by_slug.get(data["author"]),
                "is_published": True, "published_at": timezone.now() - timezone.timedelta(days=data["days_ago"]),
            })

        for order, (cat_slug, q_uz, q_ru, q_en, answer) in enumerate(FAQS):
            FAQ.objects.update_or_create(question=q_uz, defaults={
                "question_ru": q_ru, "question_en": q_en, "answer": answer,
                "category": categories.get(cat_slug), "order": order, "is_active": True,
            })

        for order, (name, position, text) in enumerate(TESTIMONIALS):
            Testimonial.objects.update_or_create(author_name=name, defaults={
                "author_position": position, "text": text, "order": order,
                "consent_received": True, "is_published": True,
            })

        self.stdout.write(self.style.SUCCESS(
            f"Qo'shildi: {len(CATEGORIES)} yo'nalish, {sum(len(c['services']) for c in CATEGORIES)} xizmat, "
            f"{len(STAFF)} jamoa a'zosi, {len(NEWS)} maqola, {len(FAQS)} savol-javob, {len(TESTIMONIALS)} sharh."
        ))
        self.stdout.write("O'chirish: python manage.py demo_data --clear")

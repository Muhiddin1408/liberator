"""Boshlang'ich ma'lumotlar: sayt sozlamalari va huquqiy sahifalar QORALAMASI.

Maxfiylik siyosati va foydalanish shartlari matni — namuna. E'lon qilishdan
oldin firma yuristlari tomonidan ko'rib chiqilishi va admin panelda
(Huquqiy sahifalar) tahrirlanishi shart.
"""
from django.db import migrations

PRIVACY_UZ = """
<p><strong>Diqqat: bu matn namuna. Firma yuristlari tomonidan tasdiqlanishi kerak.</strong></p>
<h2>1. Umumiy qoidalar</h2>
<p>“LIBERATOR” advokatlik firmasi (keyingi o‘rinlarda — Firma) ushbu sayt orqali olinadigan shaxsiy
ma’lumotlarni O‘zbekiston Respublikasining “Shaxsga doir ma’lumotlar to‘g‘risida”gi Qonuniga muvofiq
qayta ishlaydi.</p>
<h2>2. Qanday ma’lumotlar yig‘iladi</h2>
<ul>
<li>Murojaat formasida siz kiritgan ism, telefon raqami, email va xabar matni;</li>
<li>texnik ma’lumotlar: IP manzil, brauzer turi, tashrif buyurilgan sahifalar.</li>
</ul>
<h2>3. Ma’lumotlardan foydalanish maqsadi</h2>
<p>Ma’lumotlar faqat murojaatingizga javob berish, konsultatsiya tashkil etish va sayt ishini yaxshilash
uchun ishlatiladi. Advokatlik siri qonun bilan himoyalangan.</p>
<h2>4. Uchinchi tomon xizmatlari</h2>
<ul>
<li><strong>Tawk.to</strong> — onlayn chat (yozishmalar va texnik ma’lumotlar);</li>
<li><strong>Yandex Xaritalar</strong> — ofis joylashuvini ko‘rsatish;</li>
<li><strong>Yandex Metrika / Google Analytics</strong> — anonim tashrif statistikasi (cookie orqali).</li>
</ul>
<h2>5. Saqlash muddati va huquqlaringiz</h2>
<p>Siz o‘z ma’lumotlaringizni ko‘rish, o‘zgartirish yoki o‘chirishni so‘rashingiz mumkin. Buning uchun
saytdagi email yoki telefon orqali murojaat qiling.</p>
"""

PRIVACY_RU = """
<p><strong>Внимание: это образец текста. Должен быть утверждён юристами фирмы.</strong></p>
<h2>1. Общие положения</h2>
<p>Адвокатская фирма «LIBERATOR» (далее — Фирма) обрабатывает персональные данные, полученные через этот
сайт, в соответствии с Законом Республики Узбекистан «О персональных данных».</p>
<h2>2. Какие данные собираются</h2>
<ul>
<li>имя, номер телефона, email и текст сообщения, указанные в форме обращения;</li>
<li>технические данные: IP-адрес, тип браузера, посещённые страницы.</li>
</ul>
<h2>3. Цели использования</h2>
<p>Данные используются только для ответа на ваше обращение, организации консультации и улучшения работы
сайта. Адвокатская тайна охраняется законом.</p>
<h2>4. Сторонние сервисы</h2>
<ul>
<li><strong>Tawk.to</strong> — онлайн-чат (переписка и технические данные);</li>
<li><strong>Яндекс Карты</strong> — отображение расположения офиса;</li>
<li><strong>Яндекс Метрика / Google Analytics</strong> — анонимная статистика посещений (cookie).</li>
</ul>
<h2>5. Срок хранения и ваши права</h2>
<p>Вы можете запросить доступ к своим данным, их изменение или удаление, связавшись с нами по email или
телефону, указанным на сайте.</p>
"""

PRIVACY_EN = """
<p><strong>Note: this is a template text. It must be reviewed by the firm's lawyers.</strong></p>
<h2>1. General</h2>
<p>“LIBERATOR” law firm (the Firm) processes personal data collected through this website in accordance
with the Law of the Republic of Uzbekistan “On Personal Data”.</p>
<h2>2. Data we collect</h2>
<ul>
<li>name, phone number, email and message you enter in the request form;</li>
<li>technical data: IP address, browser type, pages visited.</li>
</ul>
<h2>3. Purpose</h2>
<p>Data is used only to respond to your request, arrange a consultation and improve the website.
Attorney-client privilege is protected by law.</p>
<h2>4. Third-party services</h2>
<ul>
<li><strong>Tawk.to</strong> — live chat (messages and technical data);</li>
<li><strong>Yandex Maps</strong> — office location map;</li>
<li><strong>Yandex Metrica / Google Analytics</strong> — anonymous visit statistics (cookies).</li>
</ul>
<h2>5. Retention and your rights</h2>
<p>You may request access to, correction or deletion of your data by contacting us via the email or phone
listed on the website.</p>
"""

TERMS_UZ = """
<p><strong>Diqqat: bu matn namuna. Firma yuristlari tomonidan tasdiqlanishi kerak.</strong></p>
<p>Saytdagi ma’lumotlar umumiy tanishtirish uchun mo‘ljallangan va yuridik maslahat hisoblanmaydi.
Aniq vaziyatingiz bo‘yicha maslahat olish uchun advokat bilan bog‘laning.</p>
<p>Sayt materiallaridan manbaga havola qilgan holda foydalanish mumkin.</p>
"""

TERMS_RU = """
<p><strong>Внимание: это образец текста. Должен быть утверждён юристами фирмы.</strong></p>
<p>Информация на сайте носит ознакомительный характер и не является юридической консультацией.
Для консультации по вашей ситуации свяжитесь с адвокатом.</p>
<p>Использование материалов сайта допускается при ссылке на источник.</p>
"""

TERMS_EN = """
<p><strong>Note: this is a template text. It must be reviewed by the firm's lawyers.</strong></p>
<p>Information on this website is for general guidance only and does not constitute legal advice.
Contact a lawyer for advice on your specific situation.</p>
<p>Website materials may be used with a reference to the source.</p>
"""


def seed(apps, schema_editor):
    SiteSettings = apps.get_model("app", "SiteSettings")
    LegalPage = apps.get_model("app", "LegalPage")
    SiteSettings.objects.get_or_create(pk=1)

    # Eski "Biz haqimizda" sahifasidagi raqamlar. Tekshirilmagan — shuning uchun NOFAOL.
    # Firma haqiqiyligini tasdiqlasa, admin panelda "Faol" belgisini qo'yadi.
    Achievement = apps.get_model("app", "Achievement")
    if not Achievement.objects.exists():
        for order, (value, uz, ru, en) in enumerate((
            ("20+", "yillik tajriba", "лет опыта", "years of experience"),
            ("1500+", "konsultatsiya", "консультаций", "consultations"),
            ("1000+", "mamnun mijozlar", "довольных клиентов", "satisfied clients"),
        )):
            Achievement.objects.create(value=value, label=uz, label_ru=ru, label_en=en, order=order, is_active=False)
    LegalPage.objects.get_or_create(kind="privacy", defaults={
        "title": "Maxfiylik siyosati", "title_ru": "Политика конфиденциальности", "title_en": "Privacy Policy",
        "body": PRIVACY_UZ, "body_ru": PRIVACY_RU, "body_en": PRIVACY_EN,
    })
    LegalPage.objects.get_or_create(kind="terms", defaults={
        "title": "Foydalanish shartlari", "title_ru": "Условия использования", "title_en": "Terms of Use",
        "body": TERMS_UZ, "body_ru": TERMS_RU, "body_en": TERMS_EN,
    })


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0007_content_leads_seo"),
    ]

    operations = [
        migrations.RunPython(seed, migrations.RunPython.noop),
    ]

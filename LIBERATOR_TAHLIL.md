# Liberator — baho va tuzatish rejasi

> ## ✅ Bajarilish holati (2026-09-18)
>
> | Band | Holat | Nima qilindi |
> |---|:---:|---|
> | A1 Shablon litsenziyasi | ✅ | Sayt o'z dizayniga o'tkazildi: ProCounsel CSS/JS, stok rasmlar, jQuery, Bootstrap, Font Awesome to'liq olib tashlandi. Hammasi o'zimizniki (CSS, SVG ikonkalar), shriftlar ochiq litsenziyali (OFL) |
> | A2 Soxta reyting/sharhlar | ✅ | "4.6 / 5k+", "Alen Martin", Lorem Ipsum, 5 yulduzlar o'chirildi. Sharhlar faqat `Testimonial` orqali va faqat "mijoz roziligi" belgilansa chiqadi |
> | A3 Begona domen | ✅ | Favicon o'zimizniki, newsletter (bracketweb'ga yuborardi) o'chirildi, Google shriftlar lokal |
> | A4 Maxfiylik siyosati, cookie | ✅ / ⏳ | `/maxfiylik-siyosati/`, `/foydalanish-shartlari/` (3 tilda, admin'da tahrirlanadi), cookie xabari, formada rozilik belgisi. **Matn namuna — yuristlar tasdiqlasin** |
> | B1 Aloqa formasi | ✅ | `ConsultationRequest` + forma (aloqa, bosh sahifa, har xizmat, har advokat, maqola sahifasida) + Telegram/email xabarnoma + admin'da holat + honeypot, vaqt tokeni, IP limit + `/rahmat/` |
> | B2 Analitika | ✅ / ⏳ | Metrika + GA4 `.env` dagi ID bilan ulanadi; maqsadlar: forma, telefon, Telegram, WhatsApp. **ID'larni olish kerak** |
> | B3 Blog | ✅ | `News` modeli, `/yangiliklar/`, bosh sahifada oxirgi 3 ta, muallif — `Staff` |
> | B4 Konversiya | ✅ | "Bepul konsultatsiya" CTA, qayta qo'ng'iroq oynasi, `tel:` havolalar, suzuvchi Telegram/WhatsApp tugmasi |
> | C1 `i18n_patterns` + hreflang | ✅ | `/uz/`, `/ru/`, `/en/`; URL bo'laklari va slug'lar ham tarjima qilingan (`/ru/uslugi/korporativnoe-pravo/`); tarjimasiz sahifa `noindex` + sitemap'dan chiqariladi; eski URL'lar 301 |
> | C2 Meta, OG | ✅ | title, description, canonical, Open Graph (rasm bilan) har sahifada |
> | C3 sitemap, robots | ✅ / ⏳ | `/sitemap.xml` (hreflang bilan), `/robots.txt`. **Search Console / Yandex Webmaster'ga qo'shish kerak** |
> | C4 Schema.org | ✅ | `LegalService`, `Person`, `Article`, `FAQPage` |
> | C5 URL'lar, slug | ✅ | `/uz/xizmatlar/<slug>/`, `/uz/aloqa/` |
> | C6 Har xizmat alohida sahifa | ✅ | Yo'nalish va har bir xizmat uchun sahifa |
> | D1–D3 DEBUG, SECRET_KEY, ALLOWED_HOSTS | ✅ / ⏳ | Hammasi `.env` dan; `DEBUG=False` standart. **Serverda yangi SECRET_KEY yarating** |
> | D4 Git'dagi fayllar | ✅ / ⏳ | `.gitignore` to'ldirildi, `static/`, `media/`, `__pycache__` git'dan chiqarildi. **`db.sqlite3` eski commitlarda qolgan — tarixni tozalash (git filter-repo) alohida qaror** |
> | D5 Zaxira | ✅ / ⏳ | `scripts/backup.sh` (baza + media, 30 kun) — cron'ga qo'shish kerak |
> | D6 CKEditor | ✅ | CKEditor 4 → `django-ckeditor-5`, yuklash faqat `is_staff`, faqat rasm |
> | D7 Himoya sozlamalari | ✅ | HTTPS, HSTS, secure cookie, nosniff; `check --deploy` toza |
> | D8 Admin | ✅ | `django-axes` (5 urinish), admin manzili `.env` dan (`ADMIN_URL`) |
> | E1–E2 Demo kontent, mega menyu | ✅ | O'chirildi |
> | E3 Kontent rejasi | ✅ / ⏳ | `seed_content`: 6 yo'nalish (to'liq tavsif), 15 xizmat, 8 FAQ, 4 maqola — 3 tilda. **Serverda yashirin qo'shiladi — yurist ko'rib chiqib yoqadi.** Advokatlar tajribasi, rasmlar, haqiqiy sharhlar — firmadan |
> | E4 Raqamlar | ✅ / ⏳ | `Achievement` modeli; eski 20+/1500+/1000+ **nofaol** holda kiritildi — firma tasdiqlasa yoqadi |
> | F1 Tarjima | ✅ | `{% translate %}` + `locale/ru`, `locale/en`; modellar uchun `LocalizedMixin` va `{{ obj\|tr:"name" }}` |
> | F2 Takroriy so'rov | ✅ | Context processor + kesh, `SiteSettings` singleton |
> | F3 O'lik fayllar | ✅ | `home/service/statistic.html`, `*_files` papkalari, `rex.txt` → `requirements.txt`; 40+ MB → 2 MB |
> | F4 Modellar | ✅ | `TextField`, `ordering`, `is_active` filtrlari |
> | F5 Til almashtirish | ✅ | Bitta usul — tilga mos URL havolalari |
> | G1 Rasmlar | ✅ | Yuklangan rasmlar avtomatik WebP'ga siqiladi (15 MB'lik rasm 57 KB), `loading="lazy"`, 5 MB cheklov |
> | G2 Frontend | ✅ | 22 ta skriptdan 10 tasi qoldi, WhiteNoise + siqish + hash'li kesh |
> | G3 404/500, alt, a11y | ✅ | O'z 404/500 sahifalari, `alt`, skip-link, fokus uslubi |
>
> Testlar: `python manage.py test app` — 34 ta test.

> ## ⏳ Qolgan ishlar (kod bilan hal bo'lmaydi — siz yoki firma)
>
> | # | Ish | Kim | Band |
> |:-:|---|---|:-:|
> | 1 | Maxfiylik siyosati va foydalanish shartlari matnini tasdiqlash (admin → Huquqiy sahifalar) | Firma yuristlari | A4 |
> | 2 | Serverda yangi `SECRET_KEY` yaratish, `.env` da `DEBUG=False` | Dasturchi | D1–D3 |
> | 3 | Eski commitlardagi `db.sqlite3` va `SECRET_KEY` ni git tarixidan tozalash (`git filter-repo` + force push) | Dasturchi (qaror bilan) | D2, D4 |
> | 4 | `scripts/backup.sh` ni serverda cron'ga qo'shish, tiklashni bir marta sinash | Dasturchi | D5 |
> | 5 | Telegram bot tokeni + chat ID, Gmail "App password" ni `.env` ga yozish | Dasturchi | B1 |
> | 6 | Yandex Metrika va GA4 ID'larini olish, maqsadlarni sozlash | Dasturchi | B2 |
> | 7 | Google Search Console va Yandex Webmaster'ga sayt + `sitemap.xml` | Dasturchi | C3 |
> | 8 | "20+ / 1500+ / 1000+" raqamlarini tasdiqlash va yoqish ("2010 yildan beri" bilan ziddiyat) | Firma | E4 |
> | 9 | Serverda `seed_content` → yurist matnlarni tekshirib yoqadi; advokatlar tajribasi va rasmlari, haqiqiy sharhlar | Firma | E3 |
> | 10 | Admin → Sayt sozlamalari: Telegram, WhatsApp, Instagram havolalari | Firma | B4 |
> | 11 | (ixtiyoriy) `Slider`, `AboutSection` modellari — bosh sahifa matnini admin'dan tahrirlash uchun | Dasturchi | 7.2–7.5 |

> **Umumiy baho: 4 / 10**
>
> | Soha | Ball | Izoh |
> |---|:---:|---|
> | Huquqiy va litsenziya | 1/10 | Shablon "Save page as" bilan olingan; soxta reyting va sharhlar saytda |
> | Xavfsizlik | 2/10 | `DEBUG=True`, `SECRET_KEY` kodda, `ALLOWED_HOSTS=["*"]`, baza git'da |
> | Biznes qiymati | 2/10 | **Aloqa formasi yo'q** — sayt hech qanday murojaat yig'maydi |
> | SEO | 1/10 | Uch til bitta URL'da, meta yo'q, sitemap yo'q, blog statik |
> | Kontent | 3/10 | Lorem Ipsum va inglizcha demo matnlar jonli saytda |
> | Kod sifati | 5/10 | Ishlaydi, lekin takrorlar, o'lik fayllar, tarjima chalkash |
> | Tuzilma | 6/10 | `conf/app/template` ajratilgan, modellar mantiqiy |

---

## ⚠️ Muhim eslatma: baho shkalasi boshqacha

MedBron bilan taqqoslamang. Bu **butunlay boshqa toifadagi** loyiha:

| | MedBron | Liberator |
|---|---|---|
| Nima | Tranzaksion platforma | Korporativ vizitka sayt |
| Murakkablik | Yuqori (to'lov, bron, saga) | Past (5 model, 7 sahifa) |
| 10/10 nimani anglatadi | Oylar davomidagi muhandislik | **2–3 haftalik ish** |

Ya'ni Liberator uchun 4/10 dan 9/10 ga chiqish — bu katta qayta yozish emas, balki **aniq 20–25 ta vazifa**. Loyiha kichik, shuning uchun mukammallikka yetish real va tez.

Va muhimi: bu loyihaning muvaffaqiyati kod sifatida emas. Sayt **mijoz olib kelishi** kerak. Hozir u buni qilmaydi — hatto texnik jihatdan mukammal bo'lganda ham qilmasdi, chunki aloqa formasi ham, Google'da topilish imkoni ham yo'q.

---

# NIMA YAXSHI QILINGAN

Avval halol tomoni — bu loyihada to'g'ri qilingan narsalar bor:

1. **Tuzilma toza.** `conf/` (sozlama), `app/` (mantiq), `template/`, `static_file/`, `media/` — bu Django'da to'g'ri ajratish. Ko'p boshlang'ich loyihalarda hammasi bitta joyda bo'ladi.
2. **Modellar domenni to'g'ri aks ettiradi.** `Staff`, `ServiceCategory` → `Service`, `Partner` — yuridik firma uchun aynan shu kerak. Ortiqcha abstraksiya yo'q.
3. **`Staff.localized_full_name` naqshi to'g'ri.** Aktiv tilga qarab maydon tanlaydi, bo'sh bo'lsa `uz` ga qaytadi. Bu yaxshi yechim — faqat u **bitta modelda** qolib ketgan (7-bo'limga qarang).
4. **i18n haqiqatan sozlangan.** `LocaleMiddleware`, `set_language` — ko'pchilik uch tilni shunchaki uchta alohida shablon bilan qiladi.
5. **Admin panel orqali boshqariladigan qism bor.** Jamoa va xizmatlar bazadan keladi — ya'ni advokat qo'shish uchun dasturchi kerak emas. Bu to'g'ri yo'nalish.
6. **Loyihaning o'z tahlili (`PROJECT_OVERVIEW.md`) kuchli.** 15 ta muammo aniq topilgan, yechimlar taklif qilingan. Bu hujjat loyihaning eng sifatli qismi.

Ya'ni poydevor yomon emas. Muammo shundaki, poydevor ustida **hali uy qurilmagan** — va bir nechta jiddiy xavf bor.

---

# A. HUQUQIY VA LITSENZIYA — 1/10

Bu bo'lim birinchi turadi, chunki bu yerdagi muammolar kod bilan emas, **firma obro'si va javobgarligi** bilan bog'liq. Va loyihaning o'z tahlilida bular umuman ko'rilmagan.

## ~~A1. 🔴 Shablon "Save page as" orqali olingan~~ ✅

> **Hal qilindi: shablon butunlay o'z dizaynimiz bilan almashtirildi (3-yo'l).**

**Muammo.** Hujjatda ochiq yozilgan: *dizayn ProCounsel HTML shablonidan "Save page as" orqali olingan*. Bu shablon — **tijorat mahsuloti**, sotiladi (ThemeForest / bracketweb). Demo sahifani yuklab olish sotib olish emas.

**Nega bu jiddiy.** Mijoz — **advokatlar byurosi**. Ya'ni:
- Mualliflik huquqini buzgan holda ishlayotgan yuridik firma — bu obro'ga tushadigan eng yomon zarba turi
- Shablon egasi da'vo qilsa, himoya argumenti yo'q
- Raqobatchi buni osongina aniqlaydi (shablon manbasi HTML'da qolgan — `bracketweb.com` havolalari hamon ishlaydi, A3 ga qarang)

**Yechim.**
1. Shablonni **rasmiy sotib oling**. Narxi odatda $20–80 — bu risk bilan solishtirganda hech narsa.
2. Litsenziya hujjatini saqlang (invoice, litsenziya raqami).
3. Yoki shablonni butunlay almashtiring: bepul litsenziyali (MIT/Bootstrap themes) yoki buyurtma dizayn.

> Men yurist emasman va bu huquqiy maslahat emas. Lekin bu savolni **loyiha egasiga darhol yetkazish kerak** — qaror u tomondan chiqsin.

## ~~A2. 🔴 Soxta sharhlar va reytinglar jonli saytda~~ ✅

**Muammo.** `about.html` da: **"4.6 Average ratings (5k+)"**, "Alen Martin" ismli soxta mijoz, 12 marta Lorem Ipsum. `index.html` da inglizcha demo testimonials.

**Nega bu jiddiy.** "5000+ mijoz, 4.6 reyting" — bu **reklamada yolg'on ma'lumot**. Ko'p mamlakatlarda (O'zbekistonda ham reklama to'g'risidagi qonunda) bu ma'muriy javobgarlikka olib keladi. Advokatlar byurosi uchun esa bu kasbiy etika masalasi ham.

**Yechim.** Darhol o'chiring. Haqiqiy sharh yo'q bo'lsa — bo'lim butunlay olib tashlansin. Bo'sh joy soxta raqamdan yaxshiroq.

**Bu eng shoshilinch vazifa** — bir soatlik ish, lekin uni ertaga emas, **bugun** qiling.

## ~~A3. 🟠 Sayt begona domenga bog'langan~~ ✅

**Muammo** (loyiha tahlilida 6-band). Favicon `bracketweb.com` dan yuklanadi. Newsletter formasi ham o'sha yerga yuboriladi.

**Ikki oqibat:**
1. **Ma'lumot oqishi:** obuna formasiga email kiritgan foydalanuvchi ma'lumoti **begona kompaniyaga** ketadi. Bu foydalanuvchi kutmagan narsa va maxfiylik buzilishi.
2. **Manba oshkor:** har bir tashrifchi brauzer konsolida saytning qayerdan olinganini ko'radi.

**Yechim.** Barcha tashqi havolalarni o'z domeningizga ko'chiring. Newsletter formasi ishlamasa — o'chiring, ishlasin desangiz — o'z modelingizni yozing.

## A4. 🟠 Maxfiylik siyosati va cookie xabari yo'q ⏳

> **QISMAN: sahifalar va cookie xabari tayyor; matnni firma yuristlari tasdiqlashi kerak**

**Muammo.** Saytda uchta uchinchi tomon xizmati ishlaydi: **Tawk.to** (chat — IP, brauzer, yozishmalar), **Yandex Maps**, **Mail.ru** (domen tasdiqlash fayli bor, demak metrika ham rejalashtirilgan).

Yuridik firmaning saytida maxfiylik siyosatining yo'qligi — bu ironiya emas, **mijoz uchun signal**. Odam maslahat so'rashdan oldin "bu firma o'z saytida qonunga rioya qiladimi?" deb qaraydi.

**Yechim.** `/privacy-policy/` va `/terms/` sahifalari (uch tilda), cookie xabarnomasi, Tawk.to va Yandex Maps'ning qanday ma'lumot yig'ishi haqida band. Bu kontent firmaning o'z yuristlari tomonidan yozilsin — ular buni siznikidan yaxshiroq qiladi.

---

# B. BIZNES QIYMATI — 2/10

Bu eng muhim bo'lim. Sayt texnik jihatdan mukammal bo'lishi mumkin, lekin **o'z vazifasini bajarmasa** — u behuda.

## ~~B1. 🔴 Aloqa formasi yo'q — sayt hech narsa yig'maydi~~ ✅

**Muammo.** `/contact` sahifasi faqat menyu ko'rsatadi. **Hech qanday forma yo'q.** `app/forms.py` mavjud, lekin ishlatilmaydi. Murojaat yuborish imkoni — faqat telefon qilish yoki Tawk.to chat (kimdir onlayn bo'lsa).

**Nega bu eng katta kamchilik.** Yuridik firma saytining **yagona biznes maqsadi** — konsultatsiya so'rovini olish. Sayt ko'rgan 100 odamdan 3–5 tasi murojaat qilishi kerak. Hozir bu raqam 0, chunki murojaat qiladigan joy yo'q.

Tawk.to yetarli emas: u faqat ish vaqtida ishlaydi, mobil qurilmada noqulay, va ko'p odam chat'ga yozishdan ko'ra forma to'ldirishni afzal ko'radi (ayniqsa nozik yuridik masala bo'lsa).

**Yechim — to'liq oqim:**

```python
class ConsultationRequest(models.Model):
    full_name    = models.CharField(max_length=150)
    phone        = models.CharField(max_length=20)
    email        = models.EmailField(blank=True)
    service      = models.ForeignKey(ServiceCategory, null=True, blank=True,
                                     on_delete=models.SET_NULL)
    message      = models.TextField()
    source_page  = models.CharField(max_length=200, blank=True)  # qaysi sahifadan
    language     = models.CharField(max_length=2)
    status       = models.CharField(max_length=20, default="new")
                   # new / contacted / in_progress / closed
    admin_note   = models.TextField(blank=True)
    ip_address   = models.GenericIPAddressField(null=True, blank=True)
    created_at   = models.DateTimeField(auto_now_add=True)
```

**Kerakli qismlar:**

| Qism | Nima uchun |
|---|---|
| ~~Forma `/contact` da **va** har bir xizmat sahifasida~~ ✅ | Odam xizmatni o'qib turib murojaat qiladi — o'sha yerda forma bo'lsin |
| ~~Email xabarnoma (firma pochtasiga)~~ ✅ | Aks holda hech kim murojaatni ko'rmaydi |
| ~~**Telegram bot xabarnomasi**~~ ✅ | O'zbekistonda eng tez kanal — advokat telefonida darhol ko'radi |
| ~~Admin panelda ro'yxat + holat~~ ✅ | Murojaat yo'qolmasin, kim javob berganini bilish |
| ~~Spam himoyasi~~ ✅ | reCAPTCHA v3 yoki honeypot maydon + rate limit |
| ~~Rahmat sahifasi~~ ✅ | Konversiya o'lchash uchun (`/thanks/`) |

**Qo'shimcha: qayta qo'ng'iroq formasi.** Header'da "Qayta qo'ng'iroq" tugmasi — faqat ism va telefon. Bu eng yuqori konversiyali forma turi, chunki to'ldirish 10 soniya oladi.

## B2. 🔴 Analitika yo'q — hech narsa o'lchanmaydi ⏳

> **QISMAN: kod tayyor; Metrika va GA4 ID'larini olib `.env` ga yozish kerak**

**Muammo.** Google Analytics, Yandex Metrika — ikkalasi ham yo'q (Mail.ru tasdiqlash fayli bor, lekin ulanmagan).

**Oqibat.** Savollarga javob yo'q: kuniga necha odam keladi? qaysi sahifadan chiqib ketadi? qaysi til ko'proq? qaysi xizmat qiziqtiradi? qidiruvdan keladimi yoki to'g'ridan-to'g'ri? Ya'ni saytni **yaxshilash uchun ma'lumot yo'q** — har qanday o'zgarish ko'r-ko'rona bo'ladi.

**Yechim.** Yandex Metrika (O'zbekistonda aniqroq ma'lumot beradi, Webvisor bilan) + Google Analytics 4. Maqsadlar (goals) sozlansin: forma yuborildi, telefon bosildi, Telegram bosildi.

## ~~B3. 🟠 Yangiliklar/blog statik — asosiy o'sish vositasi ishlamaydi~~ ✅

**Muammo.** Bosh sahifadagi blog bloki — demo kontent ("10 Simple Practices…", "Ronald Richards", "03 Feb").

**Nega muhim.** Yuridik firma uchun blog — reklamadan arzonroq va samaraliroq kanal. "Mehnat shartnomasi bekor qilinganda nima qilish kerak", "MCHJ ro'yxatdan o'tkazish bosqichlari" kabi maqolalar aynan yordam izlayotgan odamni olib keladi. Bu odam — tayyor mijoz.

**Yechim.** `News` modeli (loyiha tahlilida 7.4 da to'g'ri taklif qilingan) + `/news/` va `/news/<slug>/` sahifalari + bosh sahifada oxirgi 3 ta. Muallif `Staff` ga bog'lansin — bu advokatning shaxsiy obro'sini ham quradi.

## ~~B4. 🟠 Konversiya elementlari yo'q~~ ✅

Saytda odamni harakatga undaydigan narsa deyarli yo'q:

| Element | Hozir | Bo'lishi kerak |
|---|---|---|
| ~~Asosiy CTA tugmasi~~ ✅ | Demo tugma | "Bepul konsultatsiya" — har sahifada, header'da |
| ~~Telefon raqami~~ ✅ | Matn sifatida | `tel:` havola (mobilda bosilsin) |
| ~~Telegram / WhatsApp~~ ✅ | Yo'q | Suzuvchi tugma — O'zbekistonda eng ko'p ishlatiladigan kanal |
| ~~Xizmat sahifasi oxiri~~ ✅ | Hech narsa | Forma yoki "Shu masala bo'yicha murojaat qiling" |
| ~~Advokat sahifasi~~ ✅ | Kontaktlar bor | To'g'ridan-to'g'ri "Shu advokatga yozish" formasi |

---

# C. SEO — 1/10

Korporativ sayt uchun SEO — bu qo'shimcha emas, **mahsulotning o'zi**. Sayt Google'da topilmasa, u mavjud emas.

## ~~C1. 🔴 Uch til bitta URL'da — eng jiddiy SEO xatosi~~ ✅

**Muammo.** Til sessiyada saqlanadi (`/change-language/<code>/`). Ya'ni `/about/` sahifasi uchala tilda **bitta manzilda**.

**Oqibat:** Google faqat bitta versiyani indekslay oladi. Ruscha va inglizcha kontent — qidiruv tizimi uchun **mavjud emas**. Siz uch tilda kontent yozdingiz, lekin ikkitasi Google'ga ko'rinmaydi.

**Yechim — `i18n_patterns`:**
```python
# conf/urls.py
from django.conf.urls.i18n import i18n_patterns

urlpatterns = [path("admin/", admin.site.urls), path("i18n/", include("django.conf.urls.i18n"))]
urlpatterns += i18n_patterns(
    path("", include("app.urls")),
    prefix_default_language=True,
)
```
Natija: `/uz/about/`, `/ru/about/`, `/en/about/` — uchta indekslanadigan sahifa.

**Va `hreflang` teglari** (`base.html` `<head>` ichida):
```html
<link rel="alternate" hreflang="uz" href="https://domen.uz/uz/about/">
<link rel="alternate" hreflang="ru" href="https://domen.uz/ru/about/">
<link rel="alternate" hreflang="en" href="https://domen.uz/en/about/">
<link rel="alternate" hreflang="x-default" href="https://domen.uz/uz/about/">
```
Busiz Google uch tilni **takroriy kontent** deb hisoblaydi va reytingni tushiradi.

## ~~C2. 🔴 Meta teglar yo'q~~ ✅

Har sahifada bo'lishi shart:
```html
<title>Xizmat nomi | Liberator — Advokatlar byurosi</title>
<meta name="description" content="150–160 belgi, o'ziga xos">
<link rel="canonical" href="...">
<meta property="og:title" content="...">
<meta property="og:description" content="...">
<meta property="og:image" content="...">   <!-- Telegram'da havola tashlanganda ko'rinadi -->
```

**Amalga oshirish:** `SEOMixin` yoki har modelga `meta_title`, `meta_description` maydonlari (uch tilda). `base.html` da bloklar, har sahifa o'zinikini to'ldiradi.

**`og:image` alohida muhim:** O'zbekistonda havolalar Telegram orqali tarqaladi. Rasm bo'lmasa havola quruq matn bo'lib ko'rinadi.

## C3. 🟠 `sitemap.xml` va `robots.txt` yo'q ⏳

> **QISMAN: sitemap va robots tayyor; Search Console va Yandex Webmaster'ga qo'shish kerak**

Django'da bu 20 daqiqalik ish (`django.contrib.sitemaps`):
```python
class StaffSitemap(Sitemap):
    def items(self): return Staff.objects.filter(is_active=True)
    def location(self, obj): return reverse("team_detail", args=[obj.slug])
```
`robots.txt` da: `/admin/` yopilsin, sitemap manzili ko'rsatilsin.

**Google Search Console** va **Yandex Webmaster** ga sayt qo'shilsin — busiz indekslash sekin va nazoratsiz.

## ~~C4. 🟠 Structured data (Schema.org) yo'q~~ ✅

Yuridik firma uchun Google maxsus qo'llab-quvvatlaydigan turlar bor: `LegalService`, `Attorney`, `LocalBusiness`. Bu qo'shilsa qidiruv natijasida manzil, ish vaqti, reyting va telefon ko'rinadi — bosilish ehtimoli sezilarli oshadi.

```json
{"@context":"https://schema.org","@type":"LegalService",
 "name":"Liberator","address":{...},"telephone":"...","areaServed":"UZ",
 "founder":{"@type":"Person","name":"..."}}
```

## ~~C5. 🟡 URL'lar noto'g'ri qurilgan~~ ✅

| Hozir | Bo'lishi kerak | Nega |
|---|---|---|
| ~~`/service/3`~~ ✅ | `/uz/xizmatlar/korporativ-huquq/` | `pk` foydalanuvchiga ham, Google'ga ham hech narsa aytmaydi |
| ~~`/contact` (slashsiz)~~ ✅ | `/uz/aloqa/` | Boshqa URL'lar slash bilan — nomuvofiqlik |
| `/team/<slug>/` | ✅ to'g'ri | Slug ishlatilgan |

`ServiceCategory` va `Service` ga `slug` maydoni qo'shilsin (uch tilda bo'lsa yanada yaxshi).

## ~~C6. 🟡 Sahifalar kam va kontent yupqa~~ ✅

Hozir 7 ta sahifa. Google uchun bu juda kam. Har bir xizmat **alohida sahifa** bo'lsin (hozir hammasi bitta `service_item.html` ichida ro'yxat sifatida). 10 ta xizmat = 10 ta sahifa × 3 til = **30 ta indekslanadigan sahifa** — bu 7 ta emas.

---

# D. XAVFSIZLIK — 2/10

## ~~D1. 🔴 `DEBUG = True` productionda~~ ✅

**Oqibat.** Istalgan xato sahifasi ko'rsatadi: to'liq traceback, `settings.py` mazmuni, muhit o'zgaruvchilari, SQL so'rovlar, fayl yo'llari, o'rnatilgan paketlar. Hujumchi uchun bu — saytning to'liq xaritasi.

Uni ko'rish uchun hech narsa buzish shart emas: `/nonexistent-page-xyz` ni ochish yetadi.

## D2. 🔴 `SECRET_KEY` kodda va git'da ⏳

> **QISMAN: kalit `.env` da; serverda yangi SECRET_KEY yaratish kerak (eskisi git tarixida)**

**Oqibat.** `SECRET_KEY` bilan hujumchi: sessiya cookie'sini soxtalashtiradi (**admin sifatida kiradi**), parol tiklash tokenini yasaydi, imzolangan ma'lumotni o'zgartiradi.

**Yechim.**
```python
# settings.py
from pathlib import Path
import os
from dotenv import load_dotenv
load_dotenv(BASE_DIR / ".env")

SECRET_KEY   = os.environ["SECRET_KEY"]          # yo'q bo'lsa — darhol xato bersin
DEBUG        = os.getenv("DEBUG", "False") == "True"
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "").split(",")
```
**Muhim:** git tarixida qolgan eski kalitni **almashtiring** — `.env` ga ko'chirish yetarli emas, u tarixda saqlanib qoladi.

## ~~D3. 🔴 `ALLOWED_HOSTS = ["*"]`~~ ✅

Host header injection hujumiga ochiq: parol tiklash havolalari hujumchi domeniga yo'naltirilishi mumkin. Aniq ro'yxat yozilsin: `["liberator.uz", "www.liberator.uz"]`.

## D4. 🔴 `db.sqlite3` git'da — ma'lumot yo'qolish xavfi ⏳

> **QISMAN: git'dan chiqarildi; eski commitlardagi `db.sqlite3` ni tarixdan tozalash kerak**

**Ssenariy.** Admin 20 ta advokat, 15 ta xizmat, 10 ta yangilik qo'shdi. Dasturchi kodni yangiladi va `git push` qildi. Serverda `git pull` → **bazadagi hamma narsa lokal versiyaga almashdi**. Ikki oylik ish yo'qoldi.

Bu nazariy xavf emas — `db.sqlite3` git'da bo'lgan loyihalarda bu muntazam sodir bo'ladi.

**Yechim.** `.gitignore` ga: `db.sqlite3`, `media/`, `static/`, `__pycache__/`, `*.pyc`, `.env`, `venv/`. Va git tarixidan o'chirish (`git rm --cached db.sqlite3`).

## D5. 🟠 Zaxira nusxa strategiyasi yo'q ⏳

> **QISMAN: `scripts/backup.sh` tayyor; serverda cron'ga qo'shish va tiklashni sinash kerak**

Hozir butun sayt kontenti ikki joyda: `db.sqlite3` va `media/` papkasi. Ikkalasi ham zaxiralanmaydi.

**Yechim — kunlik avtomatik zaxira:**
```bash
0 3 * * *  sqlite3 /app/db.sqlite3 ".backup /backup/db-$(date +\%F).sqlite3"
0 4 * * *  tar czf /backup/media-$(date +\%F).tar.gz /app/media/
```
+ haftada bir marta boshqa serverga yoki bulutga nusxa. Va **tiklashni sinab ko'ring** — sinovdan o'tmagan zaxira zaxira emas.

> SQLite'ning o'zi bu sayt uchun **mutlaqo normal**. Kuniga bir necha admin o'zgarishi va o'qish uchun u PostgreSQL'dan kam emas, hatto tezroq. Muammo bazada emas — zaxira va git'da.

## ~~D6. 🟠 `django-ckeditor` — eskirgan paket~~ ✅

**Muammo.** `django-ckeditor` CKEditor 4 ni olib keladi. CKEditor 4 hayot sikli tugagan (EOL) va uning uchun XSS zaifliklari haqida ogohlantirishlar chiqqan. Bundan tashqari `ckeditor_uploader` fayl yuklash imkonini beradi.

**Ikki tekshiruv:**
1. Yuklash view'i **faqat `is_staff`** uchun ochiqmi? Ochiq bo'lsa — istalgan odam serverga fayl yuklaydi.
2. `CKEDITOR_RESTRICT_BY_USER = True` va ruxsat etilgan fayl turlari cheklanganmi?

**Yechim.** `django-ckeditor-5` yoki TinyMCE ga o'tish. Hozircha o'tolmasangiz — hech bo'lmaganda yuklash yo'lini yoping va joriy holatni tekshiring.

## ~~D7. 🟠 Standart himoya sozlamalari yo'q~~ ✅

Productionda bo'lishi kerak:
```python
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
X_FRAME_OPTIONS = "DENY"
SECURE_CONTENT_TYPE_NOSNIFF = True
```
Tekshirish: `python manage.py check --deploy` — Django o'zi ro'yxat beradi.

## ~~D8. 🟡 Admin panel himoyasi~~ ✅

- `/admin/` standart manzilda — bot hujumlari doimiy keladi
- Kuchli parol talabi, urinishlarni cheklash (`django-axes`)
- Admin foydalanuvchilar soni minimal bo'lsin

Kichik sayt uchun 2FA ortiqcha bo'lishi mumkin, lekin `django-axes` va manzilni o'zgartirish — 30 daqiqalik ish.

---

# E. KONTENT — 3/10

## ~~E1. 🔴 Lorem Ipsum va demo matn jonli saytda~~ ✅

A2 da aytilgan, lekin takrorlashga arziydi: `about.html` da **12 marta Lorem Ipsum**, bosh sahifada inglizcha demo blog postlari, "Ronald Richards", "Alen Martin".

Bu saytga kirgan mijoz uchun signal: **"bu firma o'z ishini oxirigacha qilmaydi"**. Yuridik xizmatda ishonch — sotiladigan yagona narsa.

**Yechim.** Bugun: hamma demo kontentni o'chiring. Bo'sh bo'lim soxta bo'limdan yaxshiroq. Keyin: haqiqiy kontent bilan to'ldiring.

## ~~E2. 🟠 Demo mega menyu~~ ✅

`base.html` da "Home Page 02…05", "Shop", "Pricing", "Gallery" — shablondan qolgan. Yuridik firmada do'kon ham, narx ro'yxati ham yo'q. Bu bosilganda 404 beradi yoki bo'sh sahifa ochadi.

## E3. 🟠 Kontent rejasi yo'q ⏳

> **QOLDI: kontentni firma yozadi (struktura admin panelda tayyor)**

Sayt to'ldirilishi kerak bo'lgan joylar:

| Bo'lim | Nima kerak |
|---|---|
| Firma haqida | Haqiqiy tarix, asos solingan yil, jamoa falsafasi |
| Xizmatlar | Har biri uchun 300–500 so'zlik tavsif: kimga, qanday, qancha vaqt |
| Advokatlar | Haqiqiy tajriba, ta'lim, yutuqlar, nashrlar |
| Keyslar | Anonimlashtirilgan muvaffaqiyatli ishlar ("Korxonaga 2 mlrd so'mlik da'vodan himoya") |
| Sharhlar | Haqiqiy mijozlardan, ruxsat bilan |
| FAQ | Eng ko'p beriladigan savollar — SEO uchun ham juda foydali |

Kontentni **firma yozsin**, siz strukturani bering. Ular o'z sohasini biladi.

## E4. 🟡 `CaseStatistic` — yaratilgan, lekin ishlatilmagan ⏳

> **QISMAN: `Achievement` modeli tayyor; raqamlarni firma tasdiqlab yoqishi kerak**

Model bor, admin'da ro'yxatdan o'tmagan, hech qayerda ko'rsatilmaydi. Yuridik firma uchun raqamlar kuchli argument: "1200+ yutilgan ish", "20 yillik tajriba", "98% muvaffaqiyat".

Bosh sahifada ko'rsating — lekin **haqiqiy raqamlar bilan** (A2 dagi xato takrorlanmasin).

---

# F. KOD SIFATI — 5/10

Loyihaning o'z tahlilida bu bo'lim yaxshi ochilgan. Qisqacha, ustuvorlik bo'yicha:

## ~~F1. 🟠 Tarjima yondashuvi chalkash~~ ✅

Hozir **uch xil usul** aralash:
1. `Staff` da `localized_*` property'lar (to'g'ri)
2. Boshqa modellarda shablonda `{% if current_lang == 'ru' %}` (yomon)
3. Statik matnlar HTML'da uch marta if/elif bilan (eng yomon)

**Yechim — ikki qadam:**
- **Model maydonlari:** `django-modeltranslation`. Shablonda `{{ obj.title }}` yetarli, aktiv tilga qarab o'zi tanlaydi. (Loyihada `translation.cpython-314.pyc` qoldig'i bor — demak sinab ko'rilgan, oxirigacha yetkazilmagan.)
- **Statik UI matnlar:** `{% trans %}` + `locale/*.po`. Shablonlar 2–3 barobar qisqaradi.

Natija: uchta `{% if %}` bloki o'rniga bitta o'zgaruvchi.

## ~~F2. 🟠 Har view'da takroriy so'rov~~ ✅

`ServiceCategory.objects.all()` har bir view'da qaytariladi (menyu uchun), `is_active` filtri qo'llanmaydi.

**Yechim — context processor:**
```python
# app/context_processors.py
def site_context(request):
    return {
        "menu_categories": ServiceCategory.objects.filter(is_active=True)
                             .prefetch_related("services"),
        "site": SiteSettings.load(),
    }
```
Har view'dan olib tashlanadi. Kesh qo'shilsa (`cache.get_or_set`, 15 daqiqa) — baza so'rovlari deyarli nolga tushadi.

## ~~F3. 🟡 Statik va o'lik fayllar~~ ✅

| Muammo | Yechim |
|---|---|
| ~~`home.html`, `service.html`, `statistic.html` ishlatilmaydi~~ ✅ | O'chirish |
| ~~`statistic_files/` papkasi~~ ✅ | O'chirish |
| ~~`static/` git'da, buzuq nomli fayllar (`*.js.Без названия`)~~ ✅ | `.gitignore` + tozalash |
| ~~`STATICFILES_DIRS` da bir papka ikki marta~~ ✅ | Bittasini qoldirish |
| ~~Nisbiy `url(assets/...)` yo'llari~~ ✅ | `{% static %}` ga o'tkazish |
| ~~`rex.txt` → `requirements.txt`, `django-ckeditor` yo'q~~ ✅ | Nomni o'zgartirish + to'ldirish |
| ~~`mailru-domain...html` ulanmagan~~ ✅ | URL'ga ulash yoki o'chirish |

## ~~F4. 🟡 Model kamchiliklari~~ ✅

- `ServiceCategory.description_ru/en` = `CharField(max_length=100)`, asli `TextField` — **tarjima sig'maydi va kesiladi**. `TextField` ga o'zgartiring.
- `is_active` maydonlari bor, lekin so'rovlarda ishlatilmaydi.
- `Meta.ordering` belgilanmagan bo'lsa — tartib tasodifiy bo'ladi.
- `__str__` metodlari admin panelda o'qilishi kerak.

## ~~F5. 🟡 Til almashtirish ikki xil usulda~~ ✅

`set_language` formasi + `/change-language/<code>/` — bittasi qolsin. `i18n_patterns` ga o'tgandan keyin (C1) standart `set_language` to'g'ri ishlaydi.

---

# G. TEZLIK VA UX — 4/10

## ~~G1. 🟠 Rasmlar optimizatsiya qilinmagan~~ ✅

**Muammo.** `ImageField` xom faylni saqlaydi. Admin telefondan 4 MB'lik rasm yuklasa — foydalanuvchiga o'sha 4 MB boradi. 10 ta advokat = 40 MB sahifa.

**Yechim.**
- `django-imagekit` yoki `easy-thumbnails` — avtomatik o'lcham va WebP
- `loading="lazy"` barcha rasmlarda
- Yuklashda o'lcham cheklovi (admin formasida validatsiya)

## ~~G2. 🟠 Frontend og'ir~~ ✅

jQuery + Bootstrap + Owl Carousel + GSAP + WOW.js — bu shablondan kelgan to'plam. Vizitka sayt uchun ortiqcha.

**Minimal choralar** (to'liq qayta yozmasdan):
- Ishlatilmaydigan JS/CSS fayllarini o'chirish
- `defer` atributi skriptlarda
- `django-compressor` yoki oddiy minifikatsiya
- **Whitenoise** + `ManifestStaticFilesStorage` — gzip va kesh sarlavhalari

**O'lchov:** PageSpeed Insights'da mobil ball. Hozir 30–50 atrofida bo'lishi ehtimoli katta. Maqsad: 80+.

## ~~G3. 🟡 Mobil va foydalanish qulayligi~~ ✅

- Telefon raqamlari `tel:` havola bo'lsin
- Manzil — xaritaga havola
- 404 va 500 uchun o'z sahifalari (hozir Django standart sahifasi, `DEBUG=False` da quruq matn)
- `alt` atributlari rasmlarda (SEO + qulaylik)
- Klaviatura bilan navigatsiya, kontrast

---

# YO'L XARITASI

Loyiha kichik — bu real bajariladigan reja.

## 🚨 Bugun (2–3 soat)

Bu uchtasi kechiktirilmaydi, chunki hozir zarar keltirmoqda:

1. ~~**Lorem Ipsum, soxta reyting ("4.6, 5k+"), demo sharhlar va blog postlarini o'chiring** (A2, E1)~~ ✅
2. ~~**Demo mega menyuni olib tashlang** (E2)~~ ✅
3. ~~**`DEBUG = False`, `ALLOWED_HOSTS` aniq ro'yxat** (D1, D3)~~ ✅

## Hafta 1 — Xavfsizlik va poydevor

| Vazifa | Bo'lim |
|---|---|
| ~~`.env` + `SECRET_KEY` almashtirish~~ ✅ | D2 |
| ~~`.gitignore` to'ldirish, `static/`/`media/` git'dan chiqarish~~ ✅ · ⏳ `db.sqlite3` ni git **tarixidan** tozalash | D4 |
| ~~Kunlik avtomatik zaxira skripti~~ ✅ · ⏳ serverda cron + tiklashni sinash | D5 |
| ~~`python manage.py check --deploy` bo'yicha hamma ogohlantirishni yopish~~ ✅ | D7 |
| ~~CKEditor yuklash yo'lini tekshirish/yopish~~ ✅ | D6 |
| ~~Tashqi domen havolalarini o'chirish (favicon, newsletter)~~ ✅ | A3 |
| ~~Shablon litsenziyasi masalasi~~ ✅ (shablon almashtirildi) | A1 |

## Hafta 2 — Sayt o'z ishini boshlasin

| Vazifa | Bo'lim |
|---|---|
| ~~**`ConsultationRequest` + forma + Telegram/email xabarnoma**~~ ✅ | B1 |
| ~~Qayta qo'ng'iroq tugmasi + `tel:` havolalar~~ ✅ | B4 |
| ~~Yandex Metrika + Google Analytics kodi, maqsadlar~~ ✅ · ⏳ ID'larni olib `.env` ga yozish | B2 |
| ~~`SiteSettings` singleton + context processor~~ ✅ | F2 |
| ~~`i18n_patterns` → `/uz/`, `/ru/`, `/en/`~~ ✅ | C1 |

> Ikkinchi hafta oxirida sayt **birinchi marta** murojaat yig'a boshlaydi va siz uni o'lchay olasiz. Bu eng katta o'zgarish.

## Hafta 3 — Google'da topilish

| Vazifa | Bo'lim |
|---|---|
| ~~Meta teglar, `hreflang`, canonical, Open Graph~~ ✅ | C1, C2 |
| ~~`sitemap.xml`, `robots.txt`~~ ✅ · ⏳ Search Console + Yandex Webmaster | C3 |
| ~~Schema.org `LegalService` / `Attorney`~~ ✅ | C4 |
| ~~Slug'lar, URL tuzilmasi~~ ✅ | C5 |
| ~~Har bir xizmat — alohida sahifa~~ ✅ | C6 |

## Hafta 4 — Kontent bazadan

| Vazifa | Bo'lim |
|---|---|
| ~~`News` modeli + `/news/` sahifalari~~ ✅ | B3 |
| ~~`Testimonial`~~ ✅ · ⏳ `Slider`, `AboutSection` (ixtiyoriy — hozir matn shablonda, tarjima fayllarida) | Tahlilda 7.2–7.5 |
| ~~Raqamlar bo'limi (`Achievement`)~~ ✅ · ⏳ firma raqamlarni tasdiqlab yoqishi | E4 |
| ~~`django-modeltranslation` + `{% trans %}` ga o'tish~~ ✅ | F1 |
| ~~O'lik fayllarni tozalash, `requirements.txt`~~ ✅ | F3 |

## Hafta 5 — Sifat

| Vazifa | Bo'lim |
|---|---|
| ~~Rasm optimizatsiyasi, lazy loading, WebP~~ ✅ | G1 |
| ~~Whitenoise, minifikatsiya, keraksiz JS o'chirish~~ ✅ | G2 |
| ~~404/500 sahifalari, `alt` teglar, mobil tekshiruv~~ ✅ | G3 |
| ~~Maxfiylik siyosati sahifasi va cookie xabari~~ ✅ · ⏳ matnni yuristlar tasdiqlashi | A4 |
| ⏳ Kontent to'ldirish (firma bilan birga) | E3 |

---

## Ballar qanday o'sadi

| Bosqich | Huquqiy | Xavfsizlik | Biznes | SEO | Kontent | Kod | **Umumiy** |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **Hozir** | 1 | 2 | 2 | 1 | 3 | 5 | **4** |
| Bugun | 6 | 5 | 2 | 1 | 6 | 5 | **5** |
| Hafta 1 | 8 | 9 | 2 | 1 | 6 | 6 | **6** |
| Hafta 2 | 8 | 9 | 8 | 4 | 6 | 7 | **7** |
| Hafta 3 | 8 | 9 | 8 | 9 | 6 | 7 | **8** |
| Hafta 4 | 9 | 9 | 9 | 9 | 8 | 9 | **9** |
| Hafta 5 | 10 | 9 | 10 | 9 | 9 | 9 | **9.5** |

> 10/10 ga yetish uchun shablon litsenziyasi hal qilinishi va kontent firma tomonidan to'liq to'ldirilishi kerak — bu ikkisi sizga bog'liq emas.

---

# UCHTA XULOSA

**1. Eng katta kamchilik — texnik emas.** Sayt chiroyli ko'rinadi, lekin murojaat qabul qilmaydi va Google'da topilmaydi. Ya'ni u firmaga hech narsa keltirmaydi. `ConsultationRequest` formasi va `i18n_patterns` — ikkita nisbatan kichik o'zgarish, lekin ular loyihaning qiymatini nolga yaqin holatdan haqiqiy vositaga aylantiradi. Kod tozalash keyin bo'lsa ham bo'ladi.

**2. Shablon masalasi — birinchi navbatda hal qilinsin.** Bu texnik qarz emas, javobgarlik. Mijoz — yuridik firma; ular bu riskni o'zlari baholay olishadi, lekin buning uchun ular **bilishi** kerak. Hujjatda ochiq yozilgan "Save page as" iborasi — bu aytilishi kerak bo'lgan narsa.

**3. Loyihani qayta yozmang.** Django + SQLite + admin panel — bu sayt uchun **to'g'ri tanlov**. Wagtail'ga o'tish yoki Next.js'da qayta yozish — vaqt isrofi. Mavjud poydevor yetarli darajada sog'lom, unga yetishmayotgan qismlarni qo'shish kifoya.

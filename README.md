# Liberator — advokatlik firmasi sayti

Django 5.2 · SQLite · uch til (`/uz/`, `/ru/`, `/en/`).

## Lokal ishga tushirish

```bash
python3 -m venv venv && source venv/bin/activate
pip install -r requirements-dev.txt
cp .env.example .env          # DEBUG=True qiling, SECRET_KEY bo'sh qolsa ham bo'ladi
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
python manage.py test app     # testlar
```

## Tuzilma

| Joy | Nima |
|---|---|
| `conf/settings.py` | Sozlamalar — hamma maxfiy qiymatlar `.env` dan |
| `app/models.py` | Jamoa, xizmatlar, murojaatlar, maqolalar, sharhlar, FAQ, sayt sozlamalari |
| `app/views.py`, `app/urls.py` | Sahifalar va murojaat qabul qilish |
| `app/notifications.py` | Yangi murojaat → Telegram + email |
| `app/seo.py`, `app/sitemaps.py` | Schema.org, sitemap.xml |
| `template/` | Shablonlar (`includes/` — qayta ishlatiladigan qismlar) |
| `static_file/site/` | CSS, JS, rasmlar, shriftlar (manba) |
| `locale/` | Rus va ingliz tarjimalari |
| `scripts/i18n.py` | Tarjima fayllarini yangilash (gettext o'rnatilmagan bo'lsa ham) |
| `scripts/backup.sh` | Kunlik zaxira |

Kontent (telefon, manzil, ijtimoiy tarmoqlar, xizmatlar, jamoa, maqolalar, FAQ,
maxfiylik siyosati) — **admin panelda** tahrirlanadi, kodga tegish shart emas.

## Tarjimalar

Shablonda matn o'zbekcha yoziladi: `{% translate "Aloqa" %}`. Keyin:

```bash
python scripts/i18n.py        # yangi matnlarni locale/*/django.po ga qo'shadi va .mo ni yig'adi
# .po fayllarda msgstr ni to'ldiring, so'ng:
python scripts/i18n.py compile
```

Model maydonlari: `name`, `name_ru`, `name_en`; shablonda `{{ obj|tr:"name" }}` — tarjima bo'sh bo'lsa o'zbekchasi chiqadi.

## Serverga joylash (production)

```bash
git pull
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py check --deploy
sudo systemctl restart liberator
```

`.env` da: `DEBUG=False`, yangi `SECRET_KEY`, `ALLOWED_HOSTS`, `SITE_URL`, `ADMIN_URL`,
Telegram/email sozlamalari. `db.sqlite3`, `media/`, `.env` serverda qoladi va **git'ga kirmaydi**.

gunicorn (systemd):

```
ExecStart=/srv/liberator/venv/bin/gunicorn conf.wsgi:application --bind 127.0.0.1:8000 --workers 3
```

nginx: `/media/` papkasini to'g'ridan-to'g'ri bering, qolganini gunicorn'ga proksi qiling
(`proxy_set_header X-Forwarded-Proto $scheme; proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;`).
Statik fayllarni WhiteNoise o'zi siqib, keshlab beradi.

Zaxira (cron): `0 3 * * * /srv/liberator/scripts/backup.sh`

## Uch til va SEO qanday ishlaydi

- Har til o'z manzilida, URL bo'laklari va slug'lar ham tarjima qilingan:
  `/uz/xizmatlar/korporativ-huquq/` · `/ru/uslugi/korporativnoe-pravo/` · `/en/services/corporate-law/`.
- Boshqa tildagi slug bilan kelinsa (`/ru/uslugi/korporativ-huquq/`) — 301 bilan to'g'ri manzilga.
- Har sahifada `hreflang` (uz, ru, en, x-default) va `canonical`. `sitemap.xml` da ham hreflang bor.
- Tarjimasi to'ldirilmagan sahifa (masalan, maqolaning ruscha matni yo'q) o'zbekcha matn bilan ochiladi,
  lekin `noindex` oladi va sitemap/hreflang'dan chiqariladi — Google uni dublikat deb hisoblamaydi.
  Tarjima admin'da to'ldirilishi bilan avtomatik indekslanadigan bo'ladi.
- Til faqat bosh sahifada (`/`) brauzer tiliga qarab tanlanadi; ichki sahifalarda hech qachon avtomatik yo'naltirilmaydi.

## Kontent

`python manage.py seed_content` — 6 ta amaliyot yo'nalishi, xizmatlar, savol-javoblar va 4 ta maqola
(uch tilda, matnlar `app/content/` da). Serverda yangi yozuvlar **yashirin** qo'shiladi: yurist ko'rib
chiqib, admin'da "Faol" / "E'lon qilingan" qiladi. Mavjud (admin'da kiritilgan) matnlar o'zgartirilmaydi.

Lokal ko'rish uchun: `python manage.py demo_data` (+ o'ylab topilgan jamoa va sharhlar; `--clear` bilan o'chadi).

## Google Search Console va Yandex Webmaster

Buni faqat domen egasi qila oladi (Google/Yandex hisobi kerak), taxminan 15 daqiqa:

1. **Google:** https://search.google.com/search-console → "Add property" → **URL prefix** → `https://liberator.uz/`.
2. Tasdiqlash usuli **HTML tag** → `content="..."` ichidagi kodni nusxalang →
   serverdagi `.env` ga `GOOGLE_SITE_VERIFICATION=<kod>` yozing → gunicorn'ni qayta ishga tushiring → "Verify".
3. Chap menyu **Sitemaps** → `sitemap.xml` → Submit.
4. **URL Inspection** da bosh sahifa va 2–3 ta xizmat sahifasini "Request indexing" qiling.
5. **Yandex:** https://webmaster.yandex.com → sayt qo'shish → **Meta tag** →
   `.env` ga `YANDEX_VERIFICATION=<kod>` → tasdiqlash → "Indexing → Sitemap files" → `https://liberator.uz/sitemap.xml`.
6. 1–2 haftadan keyin tekshiring: **Pages** (indekslangan sahifalar), **International targeting / hreflang** xatolari yo'qligi.

`.env` da `SITE_URL=https://liberator.uz` bo'lishi shart — sitemap, canonical va hreflang manzillari shundan olinadi.

## Birinchi joylashdan keyin

1. Google Search Console va Yandex Webmaster'ga sayt qo'shing, `https://domen/sitemap.xml` ni yuboring.
2. Yandex Metrika va GA4 ID'larini `.env` ga yozing. Maqsadlar (goals): `lead_form_submit`,
   `phone_click`, `telegram_click`, `whatsapp_click`, hamda `/rahmat/` sahifasiga tashrif.
3. Admin → "Sayt sozlamalari": Telegram, WhatsApp, ijtimoiy tarmoqlar.
4. Admin → "Huquqiy sahifalar": maxfiylik siyosati **namuna** — firma yuristlari tasdiqlasin.

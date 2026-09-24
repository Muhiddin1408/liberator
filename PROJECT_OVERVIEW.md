# Liberator — loyiha tahlili

## 1. Loyiha nima qiladi

**Liberator** — O‘zbekistondagi yuridik firma (advokatlar byurosi) uchun korporativ veb-sayt.
Sayt 3 tilda ishlaydi (**uz / ru / en**) va quyidagilarni ko‘rsatadi:

- firma haqida ma’lumot (20+ yillik tajriba, xizmat turlari);
- xizmat kategoriyalari va har bir kategoriya ichidagi xizmatlar;
- jamoa a’zolari (advokatlar) ro‘yxati va shaxsiy sahifasi;
- hamkorlar logotiplari;
- aloqa ma’lumotlari va Yandex xarita;
- Tawk.to onlayn chat.

Dizayn tayyor **"ProCounsel" HTML shabloni** (bracketweb.com)dan "Save page as" orqali olingan va Django shablonlariga aylantirilgan.

## 2. Texnologiyalar

| Qism | Nima ishlatilgan |
|---|---|
| Backend | Django 5.2.5, Python 3.12/3.14 |
| Baza | SQLite (`db.sqlite3`) |
| Rasm | Pillow, `ImageField` → `media/` |
| Matn muharriri | `django-ckeditor` (+ `ckeditor_uploader`) |
| Til | Django i18n (`LocaleMiddleware`, `set_language`) |
| Frontend | Bootstrap, jQuery, Owl Carousel, GSAP, WOW.js va h.k. (shablon JS'lari) |

> `rex.txt` (requirements) da `django-ckeditor` yo‘q — qo‘shish kerak.

## 3. Tuzilma

```
liberator/
├── conf/            # settings.py, urls.py (asosiy konfiguratsiya)
├── app/             # yagona Django ilova: models, views, admin, urls, forms
├── template/        # barcha HTML shablonlar
├── static_file/     # manba statik fayllar (STATICFILES_DIRS)
├── static/          # collectstatic natijasi (STATIC_ROOT)
├── media/           # admin orqali yuklangan rasmlar
└── db.sqlite3
```

## 4. Modellar (`app/models.py`)

| Model | Vazifasi | Qayerda ishlatiladi |
|---|---|---|
| `Staff` | Jamoa a’zosi: F.I.O, lavozim, mutaxassislik, amaliyot (uz/ru/en), rasm, telefon, email, Telegram, LinkedIn, slug, tartib, faol | `team.html`, `team_detail.html` |
| `ServiceCategory` | Xizmat kategoriyasi: nom, tavsif (uz/ru/en), rasm | Menyu (base), bosh sahifa karuseli, `service_item.html` |
| `Service` | Kategoriya ichidagi xizmat: sarlavha, tavsif (uz/ru/en) | `service_item.html` |
| `Partner` | Hamkor: nom, turi, logo, kontaktlar | `about.html` (logo karuseli) |
| `CaseStatistic` | Ishlar statistikasi (jinoiy/fuqarolik/…) | **Hech qayerda ishlatilmaydi**, admin'da ham ro‘yxatdan o‘tmagan |

`Staff` modelida yaxshi yondashuv bor: `localized_full_name`, `localized_position` kabi property'lar aktiv tilga qarab maydonni tanlaydi (bo‘sh bo‘lsa — uz ga qaytadi). Boshqa modellarda esa til tanlash shablonda `{% if current_lang == ... %}` bilan qilingan.

## 5. Sahifalar (URL → View → Shablon)

| URL | View | Shablon | Bazadan nima keladi |
|---|---|---|---|
| `/` | `DashboardView` | `index.html` | faqat `ServiceCategory` (xizmatlar karuseli) |
| `/about/` | `about` | `about.html` | `ServiceCategory` (menyu), `Partner` |
| `/team/` | `TeamListView` | `team.html` | `Staff` (to‘liq dinamik) |
| `/team/<slug>/` | `TeamDetailView` | `team_detail.html` | `Staff` (to‘liq dinamik) |
| `/contact` | `contact` | `contact.html` | faqat menyu |
| `/service/<pk>` | `service` | `service_item.html` | `ServiceCategory` + `Service` |
| `/change-language/<code>/` | `set_language_from_url` | — | til almashtirish |
| `/admin/` | Django admin | — | boshqaruv paneli |

Ishlatilmaydigan shablonlar: `home.html`, `service.html`, `statistic.html` (+ `template/statistic_files/` papkasi) — bular asl shablondan qolgan, hech bir view ularni chaqirmaydi.

## 6. Hozirgi holat: nima dinamik, nima statik

### ✅ Bazadan keladi
- Jamoa sahifasi va xodim detail sahifasi — to‘liq.
- Xizmat kategoriyalari (menyu, bosh sahifa karuseli, rasmi bilan).
- Xizmatlar ro‘yxati (`service_item.html`).
- Hamkorlar logotiplari (`about.html`).

### ❌ HTML ichiga qattiq yozilgan (statik)

| Joy | Nima statik | Rasm |
|---|---|---|
| `index.html` — slider | Sarlavha/subtitle 3 tilda `{% if %}` bilan | `slider-2-2.jpg`, shape rasmlar |
| `index.html` — "Biz haqimizda" | Firma haqida matn, tajriba yili, xizmat turlari ro‘yxati | `about-2-1.jpg`, `img.png` |
| `index.html` — testimonials | Mijoz fikrlari (ingliz tilida, shablondagi demo matn) | — |
| `index.html` — blog/yangiliklar | "10 Simple Practices…", "Ronald Richards", "03 Feb" — **demo kontent** | `blog-1-1.jpg`, `blog-user-1.jpg` |
| `about.html` — sarlavha va matn | Firma tarixi, missiya — 3 tilda if/elif | `about-3-1.jpg` |
| `about.html` — testimonials | **Lorem Ipsum** (12 marta), "Alen Martin", "4.6 Average ratings (5k+)" | `testi-3-1..4.jpg` |
| `contact.html` | Telefonlar, email, manzil, xarita koordinatasi | — |
| `base.html` — header/footer | Logo, telefonlar, email, manzil, ijtimoiy tarmoqlar, footer matni | `logo.png`, `footer-bg.png` |
| `base.html` — mega menyu | Shablondan qolgan "Home Page 02…05, Shop, Pricing, Gallery…" demo menyu | `home-1..5.jpg`, `home-dark.jpg` … |
| `base.html` — favicon | `bracketweb.com` saytidan yuklanadi (begona domen!) | — |
| `service_item.html` | Kategoriyada rasm bo‘lmasa default rasm | `service-d-1.jpg`, `service-author.png` |

## 7. Taklif: statikni bazaga o‘tkazish

**Ha, deyarli hammasini bazadan olib keladigan qilsa bo‘ladi.** Tavsiya etilgan yangi modellar:

### 7.1 `SiteSettings` (bitta yozuvli — singleton)
Butun sayt uchun umumiy ma’lumot: `logo`, `logo_light`, `favicon`, `phone_1`, `phone_2`, `email`, `address` (uz/ru/en), `map_lat`, `map_lng`, `facebook`, `telegram`, `instagram`, `youtube`, `footer_text` (uz/ru/en), `founded_year`.
→ `base.html` header/footer va `contact.html` shu yerdan oladi. Barcha sahifalarga **context processor** orqali uzatiladi (har bir view'da qayta yozmaslik uchun).

### 7.2 `Slider` / `HeroBanner`
`subtitle`, `title` (uz/ru/en), `background_image`, `button_text`, `button_url`, `order`, `is_active`.

### 7.3 `AboutSection` (yoki `Page`)
`title`, `text` (RichText, uz/ru/en), `image`, `experience_years` + `AboutItem` (xizmat turlari ro‘yxati bandlari).

### 7.4 `News` / `Article` — yangiliklar
`title`, `slug`, `short_text`, `content` (RichText, uz/ru/en), `image`, `author` (FK → `Staff`), `published_at`, `is_published`.
→ Bosh sahifada oxirgi 3 ta yangilik, alohida `/news/` va `/news/<slug>/` sahifalari.

### 7.5 `Testimonial` — mijoz fikrlari
`name`, `position`, `text` (uz/ru/en), `photo`, `rating`, `order`, `is_active`.
→ Lorem Ipsum o‘rniga haqiqiy fikrlar.

### 7.6 `CaseStatistic` dan foydalanish
Model allaqachon bor — admin'ga qo‘shib, bosh sahifada "N ta yutilgan ish", "N ta mijoz" kabi raqamlar sifatida ko‘rsatish mumkin (yoki oddiy `Counter` modeli: `label`, `value`).

### 7.7 Tarjima uchun yagona yondashuv
Hozir har bir modelda `name_ru`, `name_en` qo‘lda yozilgan, shablonda esa uzun `if/elif/else` bloklar. Ikki variant:
1. **`django-modeltranslation`** — maydonlarni avtomatik `_uz/_ru/_en` qiladi, shablonda oddiy `{{ obj.title }}` yetarli. (Loyihada `translation.cpython-314.pyc` qoldig‘i bor — avval shu sinab ko‘rilgan.)
2. `Staff` dagi kabi `_localized()` metodini umumiy **mixin** qilib, barcha modellarga qo‘llash.

Statik UI matnlar (tugmalar, sarlavhalar) uchun esa `{% trans %}` + `locale/` `.po` fayllari — bu `if current_lang` bloklarini butunlay yo‘qotadi va shablonlar 2–3 barobar qisqaradi.

## 8. Topilgan muammolar

1. **Xavfsizlik:** `SECRET_KEY` kodda ochiq, `DEBUG = True`, `ALLOWED_HOSTS = ["*"]` — productionda `.env` ga chiqarish kerak.
2. `db.sqlite3` va `__pycache__` git'ga qo‘shilgan — `.gitignore` ga qo‘shish kerak (`.gitignore` da faqat `venv` bor).
3. `static/` (collectstatic natijasi) git'da — keraksiz; bundan tashqari `*.js.Без названия` kabi buzuq nomli fayllar bor.
4. `STATICFILES_DIRS` da bir papka ikki marta yozilgan (`BASE_DIR / "static_file"` va `'static_file/'`).
5. Ba’zi `url(assets/...)` va `url(static/assets/...)` yo‘llari nisbiy — ichki sahifalarda (`/about/`) rasm topilmaydi. `{% static %}` tegi bilan yozish kerak.
6. Favicon va newsletter formasi `bracketweb.com` ga bog‘langan.
7. `base.html` dagi mega menyu (Shop, Pricing, Gallery, Home Page 02…) — demo, olib tashlash kerak.
8. Har bir view'da `ServiceCategory.objects.all()` takrorlanadi (menyu uchun) → context processor'ga chiqarish. `is_active` filtri ham qo‘llanmagan.
9. `service` view'da `services` va `service_category` bir xil so‘rov (ikki marta).
10. Til almashtirish ikki xil usulda qilingan (`set_language` form + `change-language/`) — bittasini qoldirish kifoya.
11. `ServiceCategory.description_ru/en` — `CharField(max_length=100)`, asosiy `description` esa `TextField`: tarjima qisqa matnga sig‘maydi.
12. `CaseStatistic` admin'da yo‘q, sahifada ishlatilmaydi.
13. `home.html`, `service.html`, `statistic.html` va ularning papkalari — ishlatilmaydigan fayllar.
14. `rex.txt` da `django-ckeditor` yo‘q; fayl nomini standart `requirements.txt` qilish ma’qul.
15. `mailru-domain...html` — Mail.ru domen tasdiqlash fayli, lekin URL'ga ulanmagan (ildizdan xizmat qilinmaydi).

## 9. Tavsiya etilgan ish tartibi

1. `SiteSettings` + context processor → header/footer/contact dinamik.
2. `News` modeli + sahifalari → yangiliklar bazadan.
3. `Testimonial`, `Slider`, `AboutSection` modellari → bosh sahifa va "Biz haqimizda" dinamik.
4. `django-modeltranslation` + `{% trans %}` ga o‘tish → `if/elif` bloklarni tozalash.
5. Demo menyu, keraksiz shablonlar va fayllarni o‘chirish; settings xavfsizligini tuzatish.

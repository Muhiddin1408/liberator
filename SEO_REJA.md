# Liberator — SEO rejasi (bosqichma-bosqich)

Maqsad: "advokatura", "адвокатура", "advokat", "адвокат", "advokatlik firmasi", "адвокатская фирма", "law firm", "lawyer / attorney Tashkent" so'rovlarida Google va Yandex'da yuqoriga chiqish.

Sayt ichidagi (kod) ishlar tayyor. Qolgan ishlar tartib bilan quyida. Har bosqich oldingisiga tayanadi, shuning uchun tartibni buzmang.

| Bosqich | Ish | Vaqt | Qachon |
|---|---|---|---|
| 1 | Kodni serverga chiqarish | 15 daqiqa | Bugun |
| 2 | Search Console va Yandex Webmaster | 1 soat | 1-kun |
| 3 | Analitika (GA4, Metrika) | 30 daqiqa | 1-kun |
| 4 | Xarita profillari (Google, Yandex, 2GIS) | 2–3 soat | 1-hafta |
| 5 | Admin paneldagi ma'lumotlar | 1 soat | 1-hafta |
| 6 | Sharhlar | doimiy | 2-haftadan |
| 7 | Tashqi havolalar va kataloglar | 1–2 kun | 2–4-hafta |
| 8 | Maqolalar | oyiga 2–4 ta | doimiy |
| 9 | Oylik nazorat | oyiga 1 soat | doimiy |

---

## 1-bosqich. Kodni serverga chiqarish

Oldingi SEO o'zgarishlari commit qilingan, lekin push qilinmagan. "Advokatura" bo'yicha oxirgi o'zgarishlar hali commit ham qilinmagan.

Lokal kompyuterda:

```bash
git add -A
git commit -m "SEO: advokatura"
git push origin main
```

Serverda:

```bash
cd /home/backend/liberator
git pull
source venv/bin/activate
python manage.py collectstatic --noinput
sudo systemctl restart liberator
```

Migratsiya kerak emas.

Tekshirish:

- [ ] https://liberator.uz/uz/ yorlig'ida "Advokat va advokatura Toshkentda — Liberator" turibdi
- [ ] Bosh sahifa pastida, forma ustida "Advokatura" bloki (3 ta savol-javob) chiroyli ko'rinadi
- [ ] https://liberator.uz/en/ ochiladi, brauzer yorlig'ida "Law firm in Tashkent, Uzbekistan — Liberator" turibdi
- [ ] Bosh sahifa ko'rinishi buzilmagan (sarlavha ustidagi kichik yozuv "Law firm in Tashkent" joyida)
- [ ] https://www.liberator.uz/ ochilganda https://liberator.uz/ ga o'tadi
- [ ] https://liberator.uz/sitemap.xml ochiladi

---

## 2-bosqich. Search Console va Yandex Webmaster

Bu qilinmasa qidiruv tizimi saytni sekin topadi va natijani o'lchab bo'lmaydi.

### Google Search Console

1. https://search.google.com/search-console ga kiring → "Add property" → "URL prefix" → `https://liberator.uz`
2. Tasdiqlash usuli: "HTML tag". Berilgan `content="..."` ichidagi kodni nusxalang.
3. Serverdagi `.env` fayliga yozing: `GOOGLE_SITE_VERIFICATION=<kod>`
4. `sudo systemctl restart liberator` → Search Console'da "Verify".
5. Chap menyu → Sitemaps → `sitemap.xml` kiriting → Submit.
6. URL Inspection orqali `/uz/`, `/ru/`, `/en/` bosh sahifalariga "Request indexing" bosing.

### Yandex Webmaster

1. https://webmaster.yandex.com → sayt qo'shing: `https://liberator.uz`
2. Tasdiqlash: "Meta tag". Kodni `.env` ga yozing: `YANDEX_VERIFICATION=<kod>`
3. `sudo systemctl restart liberator` → "Check".
4. Indexing → Sitemap files → `https://liberator.uz/sitemap.xml` qo'shing.
5. Site information → Regionality → "Tashkent" ni tanlang. Yandex uchun bu juda muhim.

### Bing (ixtiyoriy, 5 daqiqa)

https://www.bing.com/webmasters → "Import from Google Search Console".

- [ ] Google tasdiqlandi, sitemap yuborildi
- [ ] Yandex tasdiqlandi, sitemap yuborildi, hudud Toshkent

---

## 3-bosqich. Analitika

1. Google Analytics 4: https://analytics.google.com → property yarating → `G-XXXXXXXXXX` ID'ni oling.
2. Yandex Metrika: https://metrika.yandex.com → hisoblagich yarating → raqamli ID'ni oling. "Webvisor" ni yoqing.
3. Serverdagi `.env` ga yozing:

```
GOOGLE_ANALYTICS_ID=G-XXXXXXXXXX
YANDEX_METRIKA_ID=12345678
```

4. `sudo systemctl restart liberator`
5. GA4 ni Search Console bilan, Metrikani Webmaster bilan bog'lang (ikkalasining sozlamalarida bor).

- [ ] GA4 "Realtime" da o'z tashrifingiz ko'rinadi
- [ ] Metrikada hisoblagich yashil

---

## 4-bosqich. Xarita profillari

"Law firm" deb qidirganda eng tepada xarita va 3 ta firma chiqadi. U yerga sayt emas, shu profil tushadi. Eng katta ta'sir shu bosqichda.

Avval bitta "etalon" yozuv tayyorlang va hamma joyda **harfma-harf bir xil** ishlating:

- Nomi: `Liberator Law Firm` (inglizcha), `Liberator advokatlik firmasi` (o'zbekcha), `Адвокатская фирма Liberator` (ruscha)
- Manzil: saytning Aloqa sahifasidagi bilan aynan bir xil
- Telefon: saytdagi bilan bir xil format
- Sayt: `https://liberator.uz`

### Google Business Profile

1. https://business.google.com → "Add your business"
2. Asosiy kategoriya: **Law firm**. Qo'shimcha: Lawyer, Legal services, va ixtisosliklar (masalan, Criminal justice attorney, Family law attorney).
3. Manzil, telefon, ish vaqti, sayt.
4. Tasdiqlash (video yoki telefon orqali — Google ko'rsatgan usul).
5. Tavsif (750 belgigacha): birinchi gapda "law firm in Tashkent" bo'lsin, matnda "advokatura" va "advokat" so'zlari ham uchrasin.
6. Xizmatlar bo'limiga saytdagi barcha xizmatlarni kiriting.
7. Kamida 10 ta surat: ofis tashqi ko'rinishi, ichkarisi, jamoa, logo.

### Yandex Biznes

1. https://business.yandex.ru/sprav/ → tashkilot qo'shing
2. Kategoriya: "Адвокаты", "Юридические услуги". Tavsifda "адвокатура" so'zi bo'lsin.
3. Qolgani Google'dagi bilan bir xil. Telefon orqali tasdiqlanadi.

### 2GIS

https://account.2gis.com → kompaniya qo'shing, rubrika "Юридические услуги".

- [ ] Google profili tasdiqlandi va xaritada ko'rinadi
- [ ] Yandex Biznes tasdiqlandi
- [ ] 2GIS'da bor
- [ ] Uchalasida nom, manzil, telefon bir xil

---

## 5-bosqich. Admin paneldagi ma'lumotlar

Sayt admin panelida (Sayt sozlamalari):

1. Ijtimoiy tarmoq havolalarini to'ldiring (Telegram, Instagram, Facebook, LinkedIn). Hozir bo'sh; ular to'ldirilsa firma sxemasiga avtomatik qo'shiladi.
2. Meta tavsifni uch tilda quyidagiga almashtiring (bosh sahifaning qidiruv natijasidagi matni shu):
   - UZ: `Liberator — Toshkentdagi advokatura: advokatlik firmasi, tajribali advokat va yuristlar. Jinoyat, fuqarolik, iqtisodiy ishlar. Bepul konsultatsiya.`
   - RU: `Liberator — адвокатура в Ташкенте: адвокатская фирма, опытные адвокаты и юристы. Уголовные, гражданские, экономические дела. Бесплатная консультация.`
   - EN: `Liberator is a law firm (advokatura) in Tashkent, Uzbekistan: experienced lawyers and attorneys for criminal, civil and business matters. Free consultation.`
3. Har bir advokat sahifasida: surat, lavozim, tajriba, ixtisoslik uch tilda to'ldirilgan bo'lsin.
4. Har bir xizmat sahifasida kamida 300–500 so'z matn va 3–5 ta savol-javob bo'lsin.

- [ ] Ijtimoiy tarmoqlar kiritildi
- [ ] Barcha advokatlar suratli va to'liq
- [ ] Bo'sh yoki juda qisqa xizmat sahifasi qolmadi

---

## 6-bosqich. Sharhlar

Xaritadagi o'rin asosan sharhlar soni, bahosi va yangiligiga bog'liq.

1. Google profilidan "Ask for reviews" havolasini oling, qisqa havola va QR kod qiling.
2. Har bir muvaffaqiyatli yopilgan ishdan keyin mijozga Telegram/WhatsApp orqali havolani yuboring.
3. QR kodni ofis qabulxonasiga qo'ying.
4. Har bir sharhga 1–2 kun ichida javob yozing (salbiy bo'lsa ham, xotirjam).
5. Yandex xaritada ham xuddi shunday.

Maqsad: birinchi 3 oyda Google'da 20+, Yandex'da 10+ sharh.

Qilmang: soxta sharh sotib olmang va xodimlarga yozdirmang — profil bloklanadi.

---

## 7-bosqich. Tashqi havolalar va kataloglar

Raqobatchilardan o'zish uchun boshqa saytlar Liberator'ga havola berishi kerak.

**Yuridik kataloglar (inglizcha "law firm" uchun eng muhimi):**

- [ ] HG.org
- [ ] Lawyers.uz yoki shunga o'xshash mahalliy advokatlar katalogi
- [ ] Legal 500, Chambers (ariza topshiriladi, tanlov asosida)
- [ ] Advokatlar palatasi saytidagi ro'yxat

**Mahalliy kataloglar:**

- [ ] Golden Pages Uzbekistan
- [ ] Yellow Pages Uzbekistan
- [ ] Orginfo.uz

**Boshqa manbalar:**

- [ ] LinkedIn kompaniya sahifasi (sayt havolasi bilan)
- [ ] OAVda ekspert izohlari (Gazeta.uz, Kun.uz, Spot.uz, Norma.uz) — jurnalistlarga huquqiy mavzuda izoh bering, saytga havola so'rang
- [ ] Hamkorlar, mijoz kompaniyalar, uyushmalar saytlarida "hamkorlar" bo'limi

Qilmang: havola sotib olmang, havola almashish to'plamlariga qo'shilmang.

---

## 8-bosqich. Maqolalar

Hozir 6 ta maqola bor. Oyiga 2–4 ta yangi maqola, har biri uch tilda.

Qoida: bitta maqola — odamlar haqiqatda qidiradigan bitta aniq savol.

Inglizcha (xorijiy mijozlar uchun):

- How to register a company in Uzbekistan as a foreigner
- Work permit and visa for foreign employees in Uzbekistan
- Buying real estate in Uzbekistan as a foreign citizen
- Debt recovery in Uzbekistan: court procedure and timeline
- Divorce in Uzbekistan for foreign citizens

"Advokatura" so'zi uchun (birinchi navbatda yozing):

- Advokatura nima va advokat qanday tanlanadi / Что такое адвокатура и как выбрать адвоката / Advokatura in Uzbekistan: how the Bar works
- Advokat xizmati narxi Toshkentda / Сколько стоят услуги адвоката в Ташкенте
- Advokat va yurist farqi / Чем адвокат отличается от юриста

O'zbekcha / ruscha:

- Ajrashish tartibi va muddatlari / Как оформить развод в Узбекистане
- Aliment undirish / Взыскание алиментов
- Meros rasmiylashtirish / Оформление наследства
- Ishdan noqonuniy bo'shatish / Незаконное увольнение: что делать
- Qarzni sud orqali undirish / Взыскание долга через суд

Har bir maqolada: 800+ so'z, muallif sifatida aniq advokat, tegishli xizmat sahifasiga havola, oxirida konsultatsiyaga chaqiriq.

Mavzuni Search Console'dagi "Queries" hisobotidan ham oling: odamlar qaysi so'z bilan kelayotgan bo'lsa, shu haqida yozing.

---

## 9-bosqich. Oylik nazorat

Oyiga bir marta:

1. **Search Console → Performance**: "advokatura", "адвокатура", "advokat", "адвокат", "law firm" so'zlari bo'yicha ko'rsatishlar, bosishlar, o'rtacha o'rin.
2. **Search Console → Pages**: indekslanmagan sahifalar bormi.
3. **Yandex Webmaster → Search queries** va **Diagnostics**.
4. **Google Business Profile → Performance**: qo'ng'iroqlar, yo'nalish so'rovlari.
5. Saytdan kelgan murojaatlar soni (admin panel).

Kutiladigan natija:

- 2–4 hafta: sayt to'liq indekslanadi, firma nomi bilan qidirilganda birinchi chiqadi.
- 1–3 oy: xarita natijalarida ko'rina boshlaydi (sharhlar soniga bog'liq).
- 3–6 oy: "law firm Tashkent" kabi so'rovlarda birinchi sahifa.

Yolg'iz "law firm" so'rovi faqat Toshkentdagi foydalanuvchiga Liberator'ni ko'rsatadi; boshqa mamlakatdagi odamga o'sha yerdagi firmalar chiqadi. Topdagi o'rinni hech kim kafolatlay olmaydi — u shu bosqichlarning qanchalik izchil bajarilishiga bog'liq.

"""Ko'p beriladigan savollar — uch tilda. `category` = None bo'lsa aloqa sahifasida chiqadi."""

FAQS = [
    {
        "category": None,
        "question": ("Birinchi konsultatsiya bepulmi?", "Первая консультация бесплатная?",
                     "Is the first consultation free?"),
        "answer": (
            "Ha. Birinchi qisqa konsultatsiyada vaziyatingizni tinglaymiz, huquqiy istiqbollarni baholaymiz va keyingi qadamlarni tushuntiramiz. Ish bo‘yicha to‘liq xizmat narxi alohida kelishiladi.",
            "Да. На первой короткой консультации мы выслушаем вас, оценим правовые перспективы и объясним дальнейшие шаги. Стоимость полного ведения дела согласовывается отдельно.",
            "Yes. In a short first consultation we listen to your situation, assess the legal prospects and explain the next steps. Fees for full representation are agreed separately.",
        ),
    },
    {
        "category": None,
        "question": ("Qancha tez javob berasiz?", "Как быстро вы отвечаете?", "How quickly do you respond?"),
        "answer": (
            "Ish vaqtida saytdan kelgan murojaatlarga odatda shu kunning o‘zida, ko‘pincha bir soat ichida qo‘ng‘iroq qilamiz. Shoshilinch holatda to‘g‘ridan-to‘g‘ri telefon qiling.",
            "В рабочее время мы обычно перезваниваем по заявкам с сайта в тот же день, чаще всего в течение часа. В срочных случаях звоните напрямую.",
            "During business hours we usually call back on website requests the same day, most often within an hour. For urgent matters, please call us directly.",
        ),
    },
    {
        "category": None,
        "question": ("Onlayn maslahat berasizmi?", "Консультируете онлайн?", "Do you consult online?"),
        "answer": (
            "Ha. Telefon, Telegram, WhatsApp yoki video qo‘ng‘iroq orqali maslahat berishimiz mumkin. Hujjatlarni elektron shaklda yuborsangiz, oldindan o‘rganib chiqamiz.",
            "Да. Консультируем по телефону, в Telegram, WhatsApp или по видеосвязи. Если пришлёте документы в электронном виде, мы изучим их заранее.",
            "Yes. We can advise by phone, Telegram, WhatsApp or video call. If you send your documents electronically, we review them in advance.",
        ),
    },
    {
        "category": None,
        "question": ("Ma’lumotlarim maxfiy qoladimi?", "Мои данные останутся конфиденциальными?",
                     "Will my information stay confidential?"),
        "answer": (
            "Ha. Advokatga aytilgan barcha ma’lumotlar advokatlik siri hisoblanadi va qonun bilan himoyalanadi. Ular sizning roziligingizsiz uchinchi shaxslarga oshkor qilinmaydi.",
            "Да. Всё, что вы сообщаете адвокату, составляет адвокатскую тайну и охраняется законом. Без вашего согласия эти сведения не раскрываются третьим лицам.",
            "Yes. Everything you tell a lawyer is protected by attorney-client privilege under the law and is not disclosed to third parties without your consent.",
        ),
    },
    {
        "category": None,
        "question": ("Qaysi tillarda ishlaysiz?", "На каких языках вы работаете?", "Which languages do you work in?"),
        "answer": (
            "O‘zbek, rus va ingliz tillarida maslahat beramiz va hujjatlar tayyorlaymiz.",
            "Консультируем и готовим документы на узбекском, русском и английском языках.",
            "We advise and prepare documents in Uzbek, Russian and English.",
        ),
    },
    {
        "category": "korporativ-huquq",
        "question": ("Kompaniya ochish uchun qanday ma’lumotlar kerak?", "Что нужно для открытия компании?",
                     "What do I need to set up a company?"),
        "answer": (
            "Asosan: ta’sischilar haqida ma’lumot, kompaniya nomi, faoliyat turi, ustav kapitali miqdori va yuridik manzil. Qolgan hujjatlarni biz tayyorlaymiz va ro‘yxatdan o‘tkazish jarayonini boshqaramiz.",
            "В основном: сведения об учредителях, название компании, вид деятельности, размер уставного капитала и юридический адрес. Остальные документы готовим мы и ведём процесс регистрации.",
            "Mainly: details of the founders, the company name, business activities, the amount of charter capital and a registered address. We prepare the remaining documents and manage the registration.",
        ),
    },
    {
        "category": "jinoyat-ishlari",
        "question": ("Advokatni qachon jalb qilish kerak?", "Когда нужно привлекать адвоката?",
                     "When should I hire a lawyer?"),
        "answer": (
            "Imkon qadar erta — birinchi so‘roqdan oldin. Guvoh sifatida chaqirilgan bo‘lsangiz ham, advokat bilan maslahatlashish keyingi xatolarning oldini oladi.",
            "Как можно раньше — до первого допроса. Даже если вас вызывают свидетелем, консультация с адвокатом помогает избежать ошибок.",
            "As early as possible — before the first interview. Even if you are summoned as a witness, talking to a lawyer first helps avoid mistakes.",
        ),
    },
    {
        "category": "mehnat-huquqi",
        "question": ("Ishdan bo‘shatilsam nima qilishim kerak?", "Что делать, если меня уволили?",
                     "What should I do if I have been dismissed?"),
        "answer": (
            "Bo‘shatish to‘g‘risidagi buyruq nusxasini va hisob-kitob haqidagi ma’lumotni oling, mehnat shartnomangizni saqlang va kechiktirmasdan advokatga murojaat qiling — nizolashish muddatlari qisqa.",
            "Получите копию приказа об увольнении и сведения о расчёте, сохраните трудовой договор и без промедления обратитесь к адвокату — сроки на обжалование короткие.",
            "Get a copy of the dismissal order and your final pay statement, keep your employment contract and contact a lawyer without delay — the time limits for challenging a dismissal are short.",
        ),
    },
]

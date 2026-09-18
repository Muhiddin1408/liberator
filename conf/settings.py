"""
Liberator — Django sozlamalari.

Barcha maxfiy va muhitga bog'liq qiymatlar `.env` faylidan o'qiladi
(namuna: `.env.example`). Kodda hech qanday maxfiy qiymat saqlanmaydi.
"""
import os
from pathlib import Path

from django.core.exceptions import ImproperlyConfigured
from django.utils.translation import gettext_lazy as _
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / ".env")


def env_bool(name, default=False):
    return os.getenv(name, str(default)).strip().lower() in ("1", "true", "yes", "on")


def env_list(name, default=""):
    return [item.strip() for item in os.getenv(name, default).split(",") if item.strip()]


# --- Xavfsizlik -------------------------------------------------------------

DEBUG = env_bool("DEBUG", False)

SECRET_KEY = os.getenv("SECRET_KEY", "")
if not SECRET_KEY:
    if DEBUG:
        # Faqat lokal ishlab chiqish uchun. Productionda .env da bo'lishi shart.
        SECRET_KEY = "dev-only-insecure-key-do-not-use-in-production"
    else:
        raise ImproperlyConfigured("SECRET_KEY .env faylida ko'rsatilmagan.")

ALLOWED_HOSTS = env_list("ALLOWED_HOSTS")
if DEBUG:
    # Lokal ishlab chiqishda localhost har doim ruxsat etiladi (port ahamiyatsiz).
    ALLOWED_HOSTS += ["localhost", "127.0.0.1", "[::1]"]
CSRF_TRUSTED_ORIGINS = env_list("CSRF_TRUSTED_ORIGINS")

# Kanonik manzil: sitemap, canonical, hreflang va Open Graph havolalari uchun.
SITE_URL = os.getenv("SITE_URL", "http://127.0.0.1:8000").rstrip("/")

# nginx kabi proksi orqasida ishlasa — proksilar soni (mijoz IP'sini to'g'ri aniqlash uchun).
NUM_PROXIES = int(os.getenv("NUM_PROXIES", "0"))

# Admin panel manzili standart "admin/" emas — botlar uchun qiyinroq.
ADMIN_URL = os.getenv("ADMIN_URL", "admin/").strip("/") + "/"

if not DEBUG:
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
    SECURE_SSL_REDIRECT = env_bool("SECURE_SSL_REDIRECT", True)
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = int(os.getenv("SECURE_HSTS_SECONDS", "31536000"))
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True

SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_REFERRER_POLICY = "strict-origin-when-cross-origin"
X_FRAME_OPTIONS = "DENY"
SESSION_COOKIE_HTTPONLY = True


# --- Ilovalar ---------------------------------------------------------------

INSTALLED_APPS = [
    "jazzmin",  # admin mavzusi — django.contrib.admin dan oldin turishi shart
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "whitenoise.runserver_nostatic",
    "django.contrib.staticfiles",
    "django.contrib.sitemaps",
    "axes",
    "django_ckeditor_5",
    "app",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "app.middleware.AdminUzbekMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    # AxesMiddleware oxirida bo'lishi kerak.
    "axes.middleware.AxesMiddleware",
]

AUTHENTICATION_BACKENDS = [
    # Admin panelga parol tanlash hujumlaridan himoya.
    "axes.backends.AxesStandaloneBackend",
    "django.contrib.auth.backends.ModelBackend",
]
AXES_FAILURE_LIMIT = 5
AXES_COOLOFF_TIME = 1  # soat
AXES_RESET_ON_SUCCESS = True
AXES_LOCKOUT_PARAMETERS = [["username", "ip_address"]]
AXES_IPWARE_PROXY_COUNT = NUM_PROXIES or None

ROOT_URLCONF = "conf.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "template"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "app.context_processors.site_context",
            ],
        },
    },
]

WSGI_APPLICATION = "conf.wsgi.application"


# --- Ma'lumotlar bazasi -----------------------------------------------------
# SQLite bu hajmdagi sayt uchun yetarli. Zaxira: scripts/backup.sh

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.getenv("SQLITE_PATH", str(BASE_DIR / "db.sqlite3")),
    }
}

# Fayl keshi: gunicorn'ning bir nechta worker'i uchun umumiy (spam limiti, menyu keshi).
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.filebased.FileBasedCache",
        "LOCATION": os.getenv("CACHE_DIR", str(BASE_DIR / "var" / "cache")),
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator", "OPTIONS": {"min_length": 10}},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


# --- Tillar -----------------------------------------------------------------

LANGUAGE_CODE = "uz"
LANGUAGES = [
    ("uz", _("O'zbekcha")),
    ("ru", _("Русский")),
    ("en", _("English")),
]
LOCALE_PATHS = [BASE_DIR / "locale"]

TIME_ZONE = "Asia/Tashkent"
USE_I18N = True
USE_TZ = True


# --- Statik va media fayllar ------------------------------------------------

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "static"
STATICFILES_DIRS = [BASE_DIR / "static_file"]

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

STORAGES = {
    "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
    "staticfiles": {
        # gzip/brotli + fayl nomida hash => uzoq muddatli kesh.
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage"
        if not DEBUG
        else "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}

# Yuklanadigan rasmlar uchun cheklov (admin formasida tekshiriladi).
MAX_UPLOAD_IMAGE_MB = 5
DATA_UPLOAD_MAX_MEMORY_SIZE = 10 * 1024 * 1024
FILE_UPLOAD_MAX_MEMORY_SIZE = 10 * 1024 * 1024

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# --- Email va xabarnomalar --------------------------------------------------

EMAIL_BACKEND = os.getenv(
    "EMAIL_BACKEND",
    "django.core.mail.backends.console.EmailBackend" if DEBUG else "django.core.mail.backends.smtp.EmailBackend",
)
EMAIL_HOST = os.getenv("EMAIL_HOST", "smtp.gmail.com")
EMAIL_PORT = int(os.getenv("EMAIL_PORT", "587"))
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER", "")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD", "")
EMAIL_USE_TLS = env_bool("EMAIL_USE_TLS", True)
EMAIL_TIMEOUT = 10
DEFAULT_FROM_EMAIL = os.getenv("DEFAULT_FROM_EMAIL", EMAIL_HOST_USER or "noreply@liberator.uz")
SERVER_EMAIL = DEFAULT_FROM_EMAIL

# Yangi murojaatlar shu manzillarga yuboriladi (vergul bilan ajrating).
LEAD_NOTIFY_EMAILS = env_list("LEAD_NOTIFY_EMAILS")

# Telegram bot orqali murojaat xabarnomasi.
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")

# Bitta IP dan soatiga nechta murojaat qabul qilinadi (spam himoyasi).
LEAD_RATE_LIMIT_PER_HOUR = int(os.getenv("LEAD_RATE_LIMIT_PER_HOUR", "5"))


# --- Analitika --------------------------------------------------------------
# Bo'sh qoldirilsa skript umuman qo'shilmaydi.

YANDEX_METRIKA_ID = os.getenv("YANDEX_METRIKA_ID", "")
GOOGLE_ANALYTICS_ID = os.getenv("GOOGLE_ANALYTICS_ID", "")
TAWK_TO_ID = os.getenv("TAWK_TO_ID", "")  # masalan: 692983869eb8b3197fc2c92a/1jb52jhih
MAILRU_VERIFICATION = os.getenv("MAILRU_VERIFICATION", "aZNDKB74xxnYK3qG")
GOOGLE_SITE_VERIFICATION = os.getenv("GOOGLE_SITE_VERIFICATION", "")
YANDEX_VERIFICATION = os.getenv("YANDEX_VERIFICATION", "")


# --- CKEditor 5 -------------------------------------------------------------
# CKEditor 4 (django-ckeditor) hayot sikli tugagan — CKEditor 5 ga o'tildi.
# Rasm yuklash faqat is_staff foydalanuvchilarga ruxsat etilgan.

CKEDITOR_5_FILE_UPLOAD_PERMISSION = "staff"
CKEDITOR_5_ALLOW_ALL_FILE_TYPES = False
CKEDITOR_5_UPLOAD_FILE_TYPES = ["jpeg", "jpg", "png", "webp"]
CKEDITOR_5_CONFIGS = {
    "default": {
        "language": "uz",  # muharrir tugmalari o'zbekcha
        "toolbar": [
            "heading", "|", "bold", "italic", "underline", "link", "|",
            "bulletedList", "numberedList", "blockQuote", "|",
            "imageUpload", "insertTable", "|", "undo", "redo",
        ],
        "heading": {
            "options": [
                {"model": "paragraph", "title": "Oddiy matn", "class": "ck-heading_paragraph"},
                {"model": "heading2", "view": "h2", "title": "Sarlavha 2", "class": "ck-heading_heading2"},
                {"model": "heading3", "view": "h3", "title": "Sarlavha 3", "class": "ck-heading_heading3"},
            ]
        },
    },
}


# --- Admin panel (Jazzmin) ---------------------------------------------------

JAZZMIN_SETTINGS = {
    "site_title": "Liberator Admin",
    "site_header": "Liberator",
    "site_brand": "Liberator",
    "site_logo": "site/img/apple-touch-icon.png",
    "login_logo": "site/img/logo.png",
    "site_logo_classes": "img-circle elevation-2",
    "site_icon": "site/img/favicon-32.png",
    "welcome_sign": "Liberator boshqaruv paneliga xush kelibsiz",
    "copyright": "“LIBERATOR” advokatlik firmasi",
    "search_model": ["app.ConsultationRequest"],
    "user_avatar": None,
    "topmenu_links": [
        {"name": "Bosh sahifa", "url": "admin:index"},
        {"name": "Yangi murojaatlar", "url": "/{}app/consultationrequest/?status__exact=new".format(ADMIN_URL)},
        {"name": "Saytni ochish", "url": "/", "new_window": True},
    ],
    "usermenu_links": [
        {"name": "Saytni ochish", "url": "/", "new_window": True, "icon": "fas fa-globe"},
    ],
    "show_sidebar": True,
    "navigation_expanded": True,
    "hide_apps": ["axes"],
    "order_with_respect_to": [
        "app",
        "app.ConsultationRequest",
        "app.SiteSettings",
        "app.ServiceCategory",
        "app.Service",
        "app.Staff",
        "app.News",
        "app.FAQ",
        "app.Testimonial",
        "app.Achievement",
        "app.Partner",
        "app.LegalPage",
        "app.CaseStatistic",
        "auth",
    ],
    "icons": {
        "auth": "fas fa-users-cog",
        "auth.user": "fas fa-user",
        "auth.Group": "fas fa-users",
        "app.ConsultationRequest": "fas fa-inbox",
        "app.SiteSettings": "fas fa-cog",
        "app.ServiceCategory": "fas fa-balance-scale",
        "app.Service": "fas fa-gavel",
        "app.Staff": "fas fa-user-tie",
        "app.News": "fas fa-newspaper",
        "app.FAQ": "fas fa-question-circle",
        "app.Testimonial": "fas fa-comment-dots",
        "app.Achievement": "fas fa-chart-line",
        "app.Partner": "fas fa-handshake",
        "app.LegalPage": "fas fa-file-contract",
        "app.CaseStatistic": "fas fa-folder-open",
    },
    "default_icon_parents": "fas fa-chevron-circle-right",
    "default_icon_children": "fas fa-circle",
    "related_modal_active": True,
    "custom_css": "site/css/admin.css",
    "use_google_fonts_cdn": False,
    "show_ui_builder": False,
    # Uch tilli maydonlar (O'zbekcha / Русский / English) tablarga ajraladi.
    "changeform_format": "horizontal_tabs",
    "changeform_format_overrides": {
        "auth.user": "collapsible",
        "auth.group": "vertical_tabs",
        "app.consultationrequest": "single",
    },
    "language_chooser": False,
}

JAZZMIN_UI_TWEAKS = {
    "navbar": "navbar-dark",
    "no_navbar_border": True,
    "navbar_fixed": True,
    "sidebar_fixed": True,
    "sidebar": "sidebar-dark-warning",
    "sidebar_nav_child_indent": True,
    "sidebar_nav_flat_style": True,
    "brand_colour": "navbar-dark",
    "accent": "accent-warning",
    "theme": "default",
    "button_classes": {
        "primary": "btn-primary",
        "secondary": "btn-outline-secondary",
        "info": "btn-outline-secondary",
        "warning": "btn-warning",
        "danger": "btn-danger",
        "success": "btn-success",
    },
}


# --- Loglar -----------------------------------------------------------------

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {"console": {"class": "logging.StreamHandler"}},
    "root": {"handlers": ["console"], "level": "WARNING"},
    "loggers": {
        "app": {"handlers": ["console"], "level": "INFO", "propagate": False},
    },
}

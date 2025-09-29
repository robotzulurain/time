from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = "dev-secret-key"
DEBUG = True
ALLOWED_HOSTS = ["*"]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',
    'corsheaders',
    'amr_reports',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',

    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = "amr_project.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "amr_project.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

AUTH_PASSWORD_VALIDATORS = []

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

STATIC_URL = "static/"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# --- CORS (development only) ---





# --- DRF ---
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.TokenAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.AllowAny",
    ],
}


CORS_ALLOW_CREDENTIALS = True
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]
CSRF_TRUSTED_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]


# ---------- production static & WhiteNoise (added by deploy helper) ----------
import os
from pathlib import Path

# Ensure BASE_DIR exists (Django default usually defines it earlier)
try:
    BASE_DIR
except NameError:
    BASE_DIR = Path(__file__).resolve().parent.parent

# Static files (collected to this directory)
STATIC_ROOT = Path(BASE_DIR) / "staticfiles"
STATIC_URL = "/static/"

# Use WhiteNoise storage (compressed + manifest)
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# Ensure whitenoise middleware is present
try:
    if 'whitenoise.middleware.WhiteNoiseMiddleware' not in MIDDLEWARE:
        MIDDLEWARE = ['whitenoise.middleware.WhiteNoiseMiddleware'] + list(MIDDLEWARE)
except NameError:
    MIDDLEWARE = ['whitenoise.middleware.WhiteNoiseMiddleware']

# Proxy SSL header for Render / similar platforms
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
# --------------------------------------------------------------------------

# --- Netlify frontend origin (added for deployment) ---
NETLIFY_ORIGIN = "https://timeamr.netlify.app"   # replace if you choose a different Netlify site name

# Ensure Netlify origin is allowed for CORS and CSRF
try:
    if 'CORS_ALLOWED_ORIGINS' in globals():
        if NETLIFY_ORIGIN not in CORS_ALLOWED_ORIGINS:
            CORS_ALLOWED_ORIGINS.append(NETLIFY_ORIGIN)
    else:
        CORS_ALLOWED_ORIGINS = ["http://localhost:3000", NETLIFY_ORIGIN]
except Exception:
    CORS_ALLOWED_ORIGINS = ["http://localhost:3000", NETLIFY_ORIGIN]

try:
    if 'CSRF_TRUSTED_ORIGINS' in globals():
        if NETLIFY_ORIGIN not in CSRF_TRUSTED_ORIGINS:
            CSRF_TRUSTED_ORIGINS.append(NETLIFY_ORIGIN)
    else:
        CSRF_TRUSTED_ORIGINS = ["http://localhost:3000", NETLIFY_ORIGIN]
except Exception:
    CSRF_TRUSTED_ORIGINS = ["http://localhost:3000", NETLIFY_ORIGIN]
# -----------------------------------------------------

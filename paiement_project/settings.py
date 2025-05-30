from pathlib import Path
from decouple import config
import os

BASE_DIR = Path(__file__).resolve().parent.parent

# Clés secrètes et PayDunya depuis .env
SECRET_KEY = config('DJANGO_SECRET_KEY')
PAYDUNYA_MASTER_KEY = config('PAYDUNYA_MASTER_KEY')
PAYDUNYA_PRIVATE_KEY = config('PAYDUNYA_PRIVATE_KEY')
PAYDUNYA_PUBLIC_KEY = config('PAYDUNYA_PUBLIC_KEY')
PAYDUNYA_TOKEN = config('PAYDUNYA_TOKEN')

DEBUG = False  # En prod, toujours False !

# Remplace ce domaine par celui fourni par Render ou ton propre domaine
ALLOWED_HOSTS = ['django-1-sewb.onrender.com', '127.0.0.1', 'localhost']

# Applications installées
INSTALLED_APPS = [
    "corsheaders",  # Doit être en premier
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "paiement",
]

# Middleware
MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",  # En premier
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",  # Pour servir les fichiers statiques en prod
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "paiement_project.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "paiement_project.wsgi.application"

# Base de données Render (PostgreSQL ou SQLite en local)
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": config("DB_NAME"),
        "USER": config("DB_USER"),
        "PASSWORD": config("DB_PASSWORD"),
        "HOST": config("DB_HOST"),
        "PORT": config("DB_PORT", default="5432"),
    }
}

# Validation des mots de passe
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# Langue et fuseau horaire
LANGUAGE_CODE = "fr-fr"
TIME_ZONE = "Africa/Dakar"
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Fichiers statiques
STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# Fichiers médias (si tu en as besoin)
MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

# CORS (autorise tous les domaines pendant le dev, restreins en prod finale)
CORS_ALLOW_ALL_ORIGINS = True
# Pour restreindre :
# CORS_ALLOWED_ORIGINS = ['https://ton-site.com']

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

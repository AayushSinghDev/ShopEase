"""
LOCAL DEVELOPMENT SETTINGS
Usage: python manage.py runserver --settings=ShopEase.settings_local
"""
from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'shopease-local-dev-secret-key-change-in-prod'
DEBUG = True
ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'accounts', 'products', 'orders', 'discounts', 'dashboard', 'chatbot',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'ShopEase.urls'

TEMPLATES = [{'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'DIRS': [BASE_DIR / 'templates'], 'APP_DIRS': True,
    'OPTIONS': {'context_processors': [
        'django.template.context_processors.debug',
        'django.template.context_processors.request',
        'django.contrib.auth.context_processors.auth',
        'django.contrib.messages.context_processors.messages',
    ]},
}]

WSGI_APPLICATION = 'ShopEase.wsgi.application'

# ── MySQL for Local Development ──
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'shopease_db',
        'USER': 'root',
        'PASSWORD': 'root',        # Apna MySQL password yahan
        'HOST': 'localhost',
        'PORT': '3306',
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            'charset': 'utf8mb4',
        },
    }
}

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kolkata'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static'] if (BASE_DIR / 'static').exists() else []
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
SESSION_ENGINE = 'django.contrib.sessions.backends.db'
SESSION_COOKIE_AGE = 86400

# ── Email ── (Gmail App Password)
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'YOUR_GMAIL@gmail.com'           # << apna gmail
EMAIL_HOST_PASSWORD = 'YOUR_16_CHAR_APP_PASSWORD'  # << Gmail App Password
DEFAULT_FROM_EMAIL = 'ShopEase <YOUR_GMAIL@gmail.com>'

# ── Razorpay ──
RAZORPAY_KEY_ID = 'rzp_test_YOUR_KEY_HERE'
RAZORPAY_KEY_SECRET = 'YOUR_SECRET_HERE'

# ── Anthropic AI Chatbot ──
ANTHROPIC_API_KEY = 'sk-ant-YOUR_KEY_HERE'

# ── Face Recognition (local mein kaam karta hai) ──
ENABLE_FACE_RECOGNITION = True

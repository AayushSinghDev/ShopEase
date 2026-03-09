"""
Django settings for ShopEase — PythonAnywhere Production
Domain: shopease-aks.pythonanywhere.com
"""
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# ── Security ──────────────────────────────────────────────────────────────────
SECRET_KEY = os.environ.get(
    'SECRET_KEY',
    'shopease-prod-9xK2mLwQ8pZnR5vY7hJ3dF6uT0cE4bA1sI!@#mno'
)
DEBUG = False
ALLOWED_HOSTS = [
    'shopease-aks.pythonanywhere.com',
    'localhost',
    '127.0.0.1',
]

# ── Apps ──────────────────────────────────────────────────────────────────────
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'accounts',
    'products',
    'orders',
    'discounts',
    'dashboard',
    'chatbot',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'ShopEase.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'ShopEase.wsgi.application'

# ── Database — PythonAnywhere MySQL (FREE) ────────────────────────────────────
# PythonAnywhere MySQL format: username$dbname
# Yahan apni actual PythonAnywhere MySQL details daalni hain (Step 4 mein guide dekho)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME':     os.environ.get('DB_NAME',     'shopease-aks$shopease'),
        'USER':     os.environ.get('DB_USER',     'shopease-aks'),
        'PASSWORD': os.environ.get('DB_PASSWORD', 'YOUR_MYSQL_PASSWORD_HERE'),
        'HOST':     os.environ.get('DB_HOST',     'shopease-aks.mysql.pythonanywhere-services.com'),
        'PORT':     '3306',
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            'charset': 'utf8mb4',
        },
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kolkata'
USE_I18N = True
USE_TZ = True

# ── Static & Media Files ──────────────────────────────────────────────────────
# PythonAnywhere pe static files ka path:
# /home/shopease-aks/shopease_final/staticfiles/
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/'

# ── Razorpay ──────────────────────────────────────────────────────────────────
# razorpay.com pe free account banao → Dashboard → API Keys → Test Keys copy karo
RAZORPAY_KEY_ID     = os.environ.get('RAZORPAY_KEY_ID',     'rzp_test_YOUR_KEY_HERE')
RAZORPAY_KEY_SECRET = os.environ.get('RAZORPAY_KEY_SECRET', 'YOUR_SECRET_HERE')

# ── Anthropic AI Chatbot ───────────────────────────────────────────────────────
# console.anthropic.com pe account banao → API Keys → Create Key
ANTHROPIC_API_KEY = os.environ.get('ANTHROPIC_API_KEY', 'your-anthropic-key-here')

# ── Email (Gmail SMTP) ────────────────────────────────────────────────────────
# ✅ YAHAN APNI DETAILS DALNI HAIN:
# Step 1: myaccount.google.com → Security → 2-Step Verification ON karo
# Step 2: Security → App Passwords → App: Mail, Device: Other "ShopEase" → Generate
# Step 3: Jo 16-char password mile woh EMAIL_HOST_PASSWORD mein daalo
EMAIL_BACKEND       = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST          = 'smtp.gmail.com'
EMAIL_PORT          = 587
EMAIL_USE_TLS       = True
EMAIL_HOST_USER     = 'YOUR_GMAIL@gmail.com'        # ← APNA GMAIL DAALO
EMAIL_HOST_PASSWORD = 'YOUR_16_CHAR_APP_PASSWORD'   # ← APP PASSWORD DAALO
DEFAULT_FROM_EMAIL  = 'ShopEase <YOUR_GMAIL@gmail.com>'  # ← APNA GMAIL DAALO

# ── Face Recognition ──────────────────────────────────────────────────────────
# PythonAnywhere pe server pe webcam nahi hoti — False rakhna
ENABLE_FACE_RECOGNITION = False
